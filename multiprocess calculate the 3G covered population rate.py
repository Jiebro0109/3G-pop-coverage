import os
import numpy as np
import geopandas as gpd
import rasterio
import pandas as pd
from rasterstats import zonal_stats
from multiprocessing import Pool

def calculate_regional_3G_covered_population_proportion(args):
    """
    Compute the proportion of the population covered by 3G (batch processing).
    """
    (reprojected_regional_boundary, population_weight, align_3G_raster_path, output_csv, year,
     region_column_name, region_id_column_name) = args

    print(f"Processing year {year}...")

    # **Load population weight data**
    with rasterio.open(population_weight) as popu_src:
        weight_data = popu_src.read(1)
        popu_transform = popu_src.transform

    # **Load 3G coverage data**
    with rasterio.open(align_3G_raster_path) as dst:
        dst_data = dst.read(1)
        dst_data = np.where(dst_data == 2, 1, dst_data)  # Convert weak signal to 1
        dst_data = np.where(dst_data != 1, 0, dst_data)  # Convert all other values to 0

    # **Compute weighted 3G coverage (batch calculation)**
    total_covered_population = weight_data * dst_data

    # **Load regional boundary data**
    gdf = gpd.read_file(reprojected_regional_boundary)

    # **Batch compute zonal statistics**
    stats = zonal_stats(
        gdf,
        total_covered_population,
        affine=popu_transform,
        stats=["sum"],  # Directly compute the weighted covered population
        nodata=np.nan
    )

    # **Organize results**
    results = []
    for i, row in gdf.iterrows():
        region_name = row.get(region_column_name, "Unknown")
        region_id = row.get(region_id_column_name, "Unknown")

        # **Handle None values**
        covered_population_rate = stats[i]["sum"] if stats[i]["sum"] is not None else 0.0

        print(f"Processed {region_name} (ID: {region_id}), {year} Covered rate: {covered_population_rate:.5f}")

        results.append({"Year": year, "Region": region_name, "Region_ID": region_id, "Covered_Population_Rate": covered_population_rate})

    # **Save CSV file**
    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False, encoding="utf-8-sig")
    print(f"3G coverage results saved to {output_csv}")

    return year, len(gdf)  # Return year and the number of processed regions


if __name__ == "__main__":
    # Set file paths
    result_folder = r"E:\3G coverage population rate\2008-2016 USA zip code 3G coverage\result data"
    generate_data_folder = r"E:\3G coverage population rate\2008-2016 USA zip code 3G coverage\generate data"
    population_weight_tif = os.path.join(generate_data_folder, 'zip_code_pop_weight_raster.tif')
    zip_code_boundary_shp = os.path.join(generate_data_folder, "reproject_us_zip_code.shp")

    # Generate task parameter list
    task_args_list = [
        (
            zip_code_boundary_shp,
            population_weight_tif,
            os.path.join(generate_data_folder, f"aligned_3G_coverage_{year}.tif"),
            os.path.join(result_folder, f"us_zip_code_area_3G_covered_rate_{year}.csv"),
            year,
            "PO_NAME",  # Field name for the region
            "ZIP_CODE",  # Field name for the region ID
        )
        for year in range(2017, 2018)
    ]

    # **Use `multiprocessing` for parallel computation**
    with Pool(processes=6) as pool:  # Use 6 CPU cores in parallel
        results = pool.map(calculate_regional_3G_covered_population_proportion, task_args_list)

    print("All yearly calculations completed.")
