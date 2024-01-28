
# Dirmanager Py
This script organizes files in directories based on their extensions and last modification dates.

## Installation
Clone the repo:

```bash
  git clone git@github.com:gabrielhamdan/dirmanager-py.git
```

### Prerequisites
Make sure you have Python installed on your machine.

### Configuration
Although optional, users can create a configuration JSON file (e.g., config.json) with their preferences. Here is a sample configuration:

```json
{
  "targetDir": "/path/to/target/directory", // Default: Standard download folder for the OS
  "delDir": "old_stuff",                    // Default: delete
  "logFile": "/path/to/log/file.txt",       // Default: None
  "expDate": 42,                            // 30
  "textDir": "text folder",                 // text
  "imgDir": "cool images",                  // image
  "audioDir": "music",                      // audio
  "zipDir": "zipped files",                 // zip
  "videoDir": "video",                      // video
  "miscDir": "other"                        // misc
}
```

The JSON file can then be passed as an argument when running the script:

```bash
  python dirmanager.py /path/to/my_config_file.json
```

## File Extensions

The script recognizes the following file extensions:

- Text: .txt, .md, .docx, .pdf
- Image: .jpg, .jpeg, .png, .gif, .bmp
- Audio: .mp3, .wav, .flac, .aac, .ogg
- Zip: .zip, .tar, .gz, .rar
- Video: .mp4, .mkv, .avi, .mov, .wmv

## Note
The script will only organize files within directories that were originally created by the script itself. It won't touch folders not originally managed by the program in order to avoid unintended modifications.

## Lessons Learned
I have gotten to tinker with Python once or twice before (also, the syntax reminds me a lot of Godot's GDScript), but this project definitely marks my first substantial dive into the language.
To be honest, I know this isn't the most original project idea, especially when it comes to using Python, but I've tried to spice things up a little bit by adding the possibility of user prefrences.
The experience turned out to be both interesting and fun, and while I'm aware that I've only scratched the surface of Python's capabilities, I'm excited about what it has to offer.

## License
[MIT](https://choosealicense.com/licenses/mit/)