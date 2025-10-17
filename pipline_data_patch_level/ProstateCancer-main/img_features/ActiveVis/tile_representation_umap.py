import marimo

__generated_with = "0.8.22"
app = marimo.App(layout_file="layouts/tile_representation_umap.grid.json")


@app.cell
def __():
    import matplotlib.pyplot as plt
    import numpy as np
    import marimo as mo
    import pandas as pd
    import altair as alt
    import seaborn as sns
    from PIL import Image
    import os
    import openslide
    return Image, alt, mo, np, openslide, os, pd, plt, sns


@app.cell
def __(mo):
    mo.md(
        f"""
        # **Interactive Image Embeddings**
        """
    )
    return


@app.cell
def __(__file__, os):
    csv_path_root = '/Users/jjiang10/Data/ProstateCancer/output/features_umap'
    Img_dir = "/Users/jjiang10/Data/ProstateCancer/Example_WSI"


    dir_path = os.path.dirname(os.path.realpath(__file__))
    return Img_dir, csv_path_root, dir_path


@app.cell
def __(Img_dir, mo, os):
    Images = [f for f in os.listdir(Img_dir) if os.path.isfile(os.path.join(Img_dir, f)) and f.endswith('.svs')]

    Img_dropdown = mo.ui.dropdown(
      options=Images,
      value=Images[0],
      label='Choose an image:'
    )
    Img_dropdown
    return Images, Img_dropdown


@app.cell
def __(mo):
    feature_options = ["CONCH", "CLAM"]
    feature_dropdown = mo.ui.dropdown(
      options=feature_options,
      value=feature_options[0],
      label='Choose an embedding method:'
    )
    feature_dropdown
    return feature_dropdown, feature_options


@app.cell
def __(mo):
    slider = mo.ui.slider(start=4, stop=50, step=2, label='Scatter size')
    slider
    return (slider,)


@app.cell
def __(
    Img_dir,
    Img_dropdown,
    csv_path_root,
    feature_dropdown,
    openslide,
    os,
    pd,
):
    selected_slide_fn = Img_dropdown.value
    abs_wsi_fn = os.path.join(Img_dir, selected_slide_fn)
    wsi_obj = openslide.OpenSlide(abs_wsi_fn)

    # load csv file with UMAP_xy, patch_xy, and patch label
    csv_path = os.path.join(csv_path_root, feature_dropdown.value)
    csv_file = os.path.join(csv_path, selected_slide_fn.replace(".svs", "_labeled_patches.csv"))
    data = pd.read_csv(csv_file).sample(10000)

    data_sub  = data[['ump_x', 'ump_y', 'patch_x', 'patch_y', 'label']]
    update_dict = {'ump_x':'UMAP0', 'ump_y':'UMAP1'}
    data_sub = data_sub.rename(columns=update_dict)
    return (
        abs_wsi_fn,
        csv_file,
        csv_path,
        data,
        data_sub,
        selected_slide_fn,
        update_dict,
        wsi_obj,
    )


@app.cell
def __(alt, controls, data_sub, mo, slider):
    alt_chart = alt.Chart(data_sub, width=600, height=600).mark_circle(size=slider.value).encode(
    x=alt.X("UMAP0:Q"),
    y=alt.Y("UMAP1:Q"),
    color = 'label'
    )

    chart = mo.ui.altair_chart(
            alt_chart.interactive() if controls.value == "Pan & Zoom" else alt_chart,
            chart_selection=controls.value == "Selection",
            legend_selection=controls.value == "Selection", 
        )

    mo.vstack([chart, controls])
    return alt_chart, chart


@app.cell
def __(mo):
    controls = mo.ui.radio(["Selection", "Pan & Zoom"], value="Selection")
    return (controls,)


@app.cell
def __(chart, mo):
    table = mo.ui.table(chart.value, page_size=5)
    return (table,)


@app.cell
def __(chart, mo, show_images, table, wsi_obj):
    mo.stop(not len(chart.value))
    loc_x_list = chart.value['patch_x']
    loc_y_list = chart.value['patch_y']
    tb_loc_x_list = table.value['patch_x']
    tb_loc_y_list = table.value['patch_y']
    # show 10 images: either the first 10 from the selection, or the first ten
    # selected in the table

    selected_images = (
        show_images(list(loc_x_list), list(loc_y_list), wsi_obj)
        if not len(table.value)
        else show_images(list(tb_loc_x_list), list(tb_loc_y_list), wsi_obj)
    )

    mo.md(
        f"""
        **Data Selected:**
        {mo.as_html(selected_images)}

        {table}
        """
    )
    return (
        loc_x_list,
        loc_y_list,
        selected_images,
        tb_loc_x_list,
        tb_loc_y_list,
    )


@app.cell
def __(np, plt):
    def show_images(loc_x_list, loc_y_list, wsi_obj):
        print("Showing images")
        # indices = [index for index in indices if os.path.isfile(index)]
        fig, axes = plt.subplots(4, 6)
        # fig.set_size_inches(12.5, 1.5)
        if len(loc_x_list) > 1:
            for loc_x, loc_y, ax in zip(loc_x_list, loc_y_list, axes.flat):
                im = wsi_obj.read_region((int(loc_x), int(loc_y)), 0, [224, 224]) 
                ax.imshow(np.array(im))
        elif len(loc_x_list) == 1:
            im = wsi_obj.read_region((int(loc_x_list[0]), int(loc_y_list[0])), 0, [224, 224])
            axes.flat[0].imshow(np.array(im))
        for ax in axes.flat:
            ax.set_yticks([])
            ax.set_xticks([])

        plt.tight_layout()
        return fig
    return (show_images,)


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
import marimo

__generated_with = "0.8.22"
app = marimo.App(layout_file="layouts/tile_representation_umap.grid.json")


@app.cell
def __():
    import matplotlib.pyplot as plt
    import numpy as np
    import marimo as mo
    import pandas as pd
    import altair as alt
    import seaborn as sns
    from PIL import Image
    import os
    import openslide
    return Image, alt, mo, np, openslide, os, pd, plt, sns


@app.cell
def __(mo):
    mo.md(
        f"""
        # **Histomorphology Image Representation**
        """
    )
    return


@app.cell
def __(__file__, os):
    csv_path_root = '/Users/jjiang10/Data/ProstateCancer/output/features_umap'
    Img_dir = "/Users/jjiang10/Data/ProstateCancer/Example_WSI"


    dir_path = os.path.dirname(os.path.realpath(__file__))
    return Img_dir, csv_path_root, dir_path


@app.cell
def __(Img_dir, mo, os):
    Images = [f for f in os.listdir(Img_dir) if os.path.isfile(os.path.join(Img_dir, f)) and f.endswith('.svs')]

    Img_dropdown = mo.ui.dropdown(
      options=Images,
      value=Images[0],
      label='Choose an image:'
    )
    Img_dropdown
    return Images, Img_dropdown


@app.cell
def __(mo):
    feature_options = ["CONCH", "CLAM"]
    feature_dropdown = mo.ui.dropdown(
      options=feature_options,
      value=feature_options[0],
      label='Choose an embedding method:'
    )
    feature_dropdown
    return feature_dropdown, feature_options


@app.cell
def __(mo):
    slider = mo.ui.slider(start=4, stop=50, step=2, label='Scatter size')
    slider
    return (slider,)


@app.cell
def __(
    Img_dir,
    Img_dropdown,
    csv_path_root,
    feature_dropdown,
    openslide,
    os,
    pd,
):
    selected_slide_fn = Img_dropdown.value
    abs_wsi_fn = os.path.join(Img_dir, selected_slide_fn)
    wsi_obj = openslide.OpenSlide(abs_wsi_fn)

    # load csv file with UMAP_xy, patch_xy, and patch label
    csv_path = os.path.join(csv_path_root, feature_dropdown.value)
    csv_file = os.path.join(csv_path, selected_slide_fn.replace(".svs", "_labeled_patches.csv"))
    data = pd.read_csv(csv_file).sample(10000)

    data_sub  = data[['ump_x', 'ump_y', 'patch_x', 'patch_y', 'label']]
    update_dict = {'ump_x':'UMAP0', 'ump_y':'UMAP1'}
    data_sub = data_sub.rename(columns=update_dict)
    return (
        abs_wsi_fn,
        csv_file,
        csv_path,
        data,
        data_sub,
        selected_slide_fn,
        update_dict,
        wsi_obj,
    )


@app.cell
def __(alt, controls, data_sub, mo, slider):
    alt_chart = alt.Chart(data_sub, width=600, height=600).mark_circle(size=slider.value).encode(
    x=alt.X("UMAP0:Q"),
    y=alt.Y("UMAP1:Q"),
    color = 'label'
    )

    chart = mo.ui.altair_chart(
            alt_chart.interactive() if controls.value == "Pan & Zoom" else alt_chart,
            chart_selection=controls.value == "Selection",
            legend_selection=controls.value == "Selection", 
        )

    mo.vstack([chart, controls])
    return alt_chart, chart


@app.cell
def __(mo):
    controls = mo.ui.radio(["Selection", "Pan & Zoom"], value="Selection")
    return (controls,)


@app.cell
def __(chart, mo):
    table = mo.ui.table(chart.value, page_size=5)
    return (table,)


@app.cell
def __(chart, mo, show_images, table, wsi_obj):
    mo.stop(not len(chart.value))
    loc_x_list = chart.value['patch_x']
    loc_y_list = chart.value['patch_y']
    tb_loc_x_list = table.value['patch_x']
    tb_loc_y_list = table.value['patch_y']
    # show 10 images: either the first 10 from the selection, or the first ten
    # selected in the table

    selected_images = (
        show_images(list(loc_x_list), list(loc_y_list), wsi_obj)
        if not len(table.value)
        else show_images(list(tb_loc_x_list), list(tb_loc_y_list), wsi_obj)
    )

    mo.md(
        f"""
        **Data Selected:**
        {mo.as_html(selected_images)}

        {table}
        """
    )
    return (
        loc_x_list,
        loc_y_list,
        selected_images,
        tb_loc_x_list,
        tb_loc_y_list,
    )


@app.cell
def __(np, plt):
    def show_images(loc_x_list, loc_y_list, wsi_obj):
        print("Showing images")
        # indices = [index for index in indices if os.path.isfile(index)]
        fig, axes = plt.subplots(4, 6)
        # fig.set_size_inches(12.5, 1.5)
        if len(loc_x_list) > 1:
            for loc_x, loc_y, ax in zip(loc_x_list, loc_y_list, axes.flat):
                im = wsi_obj.read_region((int(loc_x), int(loc_y)), 0, [224, 224]) 
                ax.imshow(np.array(im))
        elif len(loc_x_list) == 1:
            im = wsi_obj.read_region((int(loc_x_list[0]), int(loc_y_list[0])), 0, [224, 224])
            axes.flat[0].imshow(np.array(im))
        for ax in axes.flat:
            ax.set_yticks([])
            ax.set_xticks([])

        plt.tight_layout()
        return fig
    return (show_images,)


@app.cell
def __():
    return


if __name__ == "__main__":
    app.run()
