# LACCEI Video Preparer Design

The LACCEI Video Preparer is a module that assists in preparing videos for virtual conference sessions.

This document describes a design that aims to create intuitive software that automates the creation of these videos. The process involves
- gathering original videos,
- adhering to a schedule for video preparation,
- and uploading them to the target platform, YouTube.

The figure below shows the overall intended system design. 

![](laccei-video-preparer-system-diagram.png)

## System and Modules Description
This subsystem can handle all the aforementioned tasks. However, it does not implement a user-friendly interface; rather, it could be added to a larger platform (e.g., a Django site or software suite) to integrate these functionalities.

The system contains three main components.
1. Data Retriever
1. Video Preparer
1. Data Sender

The first component, the **Data Retriever**, involves contacting the platform that holds the original videos (those submitted by the conference authors) and information about the sessions (the schedule). A schedule that groups the videos into sessions and information about those sessions is needed to compile the videos.

This module will provide the schedule in a JSON format that the other modules can understand. It will also save the videos in a folder that can accessed.

The **Video Preparer** is the most important module, as it performs the main task this system is supposed to do. It creates videos for the virtual sessions by following the schedule and grouping videos within the same session. It also produces opening slides containing information about the sessions (session name and time), a closing slide, and some background music for those informative slides.

Compiling the videos can be automated using only this module, and a CLI program can be used to interact with it. That would be the simplest version of this program. The other tasks, downloading and uploading the videos, could be performed manually in that case. However, adding those functionalities through the other modules makes this system hassle-free.

Finally, the **Data Uploader** is the last stage in the pipeline. It uploads the processed videos to the target platform, YouTube. The videos' titles use the conference and session names.