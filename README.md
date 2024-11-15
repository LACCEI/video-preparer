# Video Preparer

Welcome to the Video Preparer project! This project is designed to help LACCEI prepare videos for the conferences' virtual sessions. It is still a work in progress, but the tool currently works to automate the video creation process as a python script program. 

## Design and Features

This project is designed to offer a terminal interface and a modules that can be added to bigger systems (e.g, a Django site). Get a quick intro to the project by reading the brief [design overview](design/design.md).

Overall, the project has the following features.
- **Automated Download**: Automatically retrieve the schedule and videos from ConfTool.
- **Video Preparation**: Perform multiple steps required in the process of creating the videos.
  - **Videos Resampling**: Authors produce videos in different frames per seconds and encodings (e.g., 24 FPS and 600 FPS). The program resamples all the videos for compatibility.
  - **Automated Instructions Creation**: Every conference and sessions have specific times and titles, the video creation module (vidpro) can produce the instruction slides using the session's information (e.g., start time, title, time zone, etc.).
  - **Audio Normalization**: Input videos usually all have different audio levels. This program takes care of normalizing all audio levels to the maximum possible.
  - **Proper Ordering**: Videos must appear in a certain order in the conferences. This program makes sure they are concatenated in the proper order.
  - **Video Rescaling**: Authors send their videos in different dimensions (e.g., 1080x1440, 640x360). The program takes care of resizing all videos to fit them properly in a standard dimenension.
- **Automated Upload (Pending)**: The design includes a module (namely, datasender), to automatically upload the output videos to YouTube and organize them in a Playlist.

## Installation and Usage

### Prerequisites
This program needs two binaries in the system where it is running to work properly.
- [FFMPEG](https://ffmpeg.org)
- [ImageMagick](https://imagemagick.org)

To install these programs in Debian systems, run:
```
sudo apt install ffmpeg imagemagick
```

Read the projects' sites to install in other systems (e.g., Windows).

#### Debugging
There is also an issue when running the program with a fresh installation of ImageMagick in Linux. You must edit the policy to create PDF files in `/etc/ImageMagick-6/policy.xml`. Change the line
```xml
<policy domain="coder" rights="none" pattern="PDF" />
```
to
```xml
<policy domain="coder" rights="read|write" pattern="PDF" />
```

Similarly, chage the line
```xml
<policy domain="path" rights="none" pattern="@*" />
```
to
```xml
<policy domain="path" rights="read|write" pattern="@*" />
```

### Installation

This project relies heavily in [MoviePy](https://zulko.github.io/moviepy/) and ffmpeg. ImageMagick is required to create the instruction slides.

There is a [requirements.txt](requirements.txt) file in the root directory to install all the required packages for the program. Start by creating a virtual environment.
```
python3 -m venv venv
```

Then, install the required packages.
```
pip install -r requirements.txt
```

### Preparing Script for a Conference

The project is still under development, but some parts can be used with a script with the proper configurations. The `src/vidpre.py` module is the interface between the program and any other service. The `src/vidprecli.py` will be a program program that interfaces `vidpre.py` and prepares the configuration of the task through the terminal.

Meanwhile, using a script like `src/laccei_2024.py` is useful in using some components of the project to automate tasks. Read that script and use it as a reference to create a different one for a different conference.

Note that you can create a `.env` file in the root directory with the ConfTool API keys.
```
CONFERENCE_ENDPOINT = "[paste endpoint here]"
PASSWORD = "[paste the password here]"
```

#### Windows

If the program is running on Windows, there will be issues when the program tries to communicate with ffmpeg or ImageMagick. In that case, add the path to the programs by editing the environment variables adding the following lines to the [`src/vidpro/__init__.py`](src/vidpro/__init__.py) file before the first import of the MoviePy module.
```python
os.environ["IMAGEIO_FFMPEG_EXE"] = "C:/Programs File/path/to/ffmpeg.exe"
os.environ["IMAGEMAGICK_BINARY"] = "C:/Programs File/path/to/magick.exe"
```

Note that the path uses forward slashes and end with the `.exe` extension.

### Optimizations

There are some optimization currenlty in place to speed up the video processing. However, it could be significantly faster. If there is a GPU with the [proper transcoding functionalities](https://stackoverflow.com/a/63585334), it is possible to enable the proper flags when calling ffmpeg to speed up the proces. That is done mostly in the vidpro and vidpre modules. Those optimizations could be added to the program to automatically detect and use these optimizations.

## Future Development
Roadmap for future work:
- [ ] Develop interface to upload videos to YouTube.
- [ ] Create source code documentation.
- [ ] Improve logging and error loging systems.
- [ ] Complete the `vidpre.py` interface.
