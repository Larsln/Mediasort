
# Mediasort

Mediasort is a tool for automatic media file sorting and adding geo-tags based on a reference file.

---

## 🚀 Quick Start with Docker Compose

1. Create a `.env` file:

    ```bash
    ONLY_SORT=True
    INPUT_PATH=./input
    OUTPUT_PATH=./output
    ```

    **Note**: Adjust the paths according to your system setup.

2. In every subfolder containing photos, add a `reference.txt` file with GPS coordinates in decimal format if you want to add geo-tags to non tagged Photos & Videos. The format should be:

    ```
    Latitude, Longitude, [optional Altitude]
    e.g.
    48.137154, 11.576124, 520
    ```

3. Start the program with:

    ```bash
    docker compose up
    ```

---

## 🗂️ How It Works

- The program reads `INPUT_PATH` and `OUTPUT_PATH` from the environment variables.
- In each subfolder under `INPUT_PATH` that contains a `reference.txt` file, all photos missing geo-tags will be tagged with the GPS coordinates from that file.
- Then, media files are automatically sorted and moved into the appropriate folder structure in `OUTPUT_PATH`.

### Sorting Scheme

The sorting scheme is:

```
Country/Year/City/2025_03_03_DEVICE_SERIALNUMBER_SEQUENCE.extension
```

---

## 📁 Reference.txt File

- Must be placed in the same folder as the photos to be tagged.
- Must contain GPS coordinates in decimal format (latitude, longitude), altitude is optional.

**Example**:

```
48.137154, 11.576124, 520
```

---

## ⚙️ Configuration via Environment Variables

| Variable     | Description                                      | Example     |
|--------------|--------------------------------------------------|-------------|
| `ONLY_SORT`  | If `True`, only sorting is done, no geo-tagging  | `True`      |
| `INPUT_PATH` | Path to the folder with the input media files    | `./input`   |
| `OUTPUT_PATH`| Path to the folder for the sorted output files   | `./output`  |

---

## 🔧 Requirements

- Docker and Docker Compose must be installed.
- The folder structure under `INPUT_PATH` should contain photos and the `reference.txt` files.

---

## 📝 Feedback & Issues

If you encounter problems or have suggestions, please open an issue in the repository.
```
