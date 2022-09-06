<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">SF Compare and Load</h3>

  <p align="center">
    An Org Object-Mapping SalesForce Tool
    <br />
    <a href="https://github.com/Nirav-TecEX/SFCompareAndLoad"><strong>LINKS »</strong></a>
    <br />
  </p>
</div>

 <!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary>
  <ol>
    <li><a href="#about-the-project">About The Project</a></li>
    <li>
      <a href="#installation">Installation</a>
      <ul>
        <li><a href="#requirements">Requirements</a></li>
      </ul>
    </li>
    <li>
      <a href="#usage">Usage</a>
      <ul>
        <li><a href="#clean-up">Clean-up</a></li>
      </ul>
    </li>
    <li>
      <a href="#debugging">Debugging</a>
      <ul>
        <li><a href="#loggers">Loggers</a></li>
      </ul>
      <ul>
        <li><a href="#outputs">Outputs</a></li>
      </ul>
    </li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#license">License</a></li>
    <li><a href="#contact">Contact</a></li>
    <li><a href="#acknowledgments">Acknowledgments</a></li>
  </ol>
</details>

<!-- ABOUT THE PROJECT -->
## About The Project

This tool is used to map _unique ids_ between orgs. It uses a matching string to do so. The project uses a .env file for defining variables. The matching string for an object can be changed in the .env file. 

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With
_No external projects._

## Installation
Head over to the directory wehre you want to install the project and perform the following:
1. Clone the repo using
    ```
    $ git clone
    ```
2. Head into the repo using:
    ```
    $ cd SFCompareAndLoad
    ```

### Requirements
Please ensure that your .env is configured correctly.     	

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage
Given that all of the requirements are met, the project can be used. In the file directory open up a powershell and run 
  ```
	$ python main.py
  ```
This will start up the server. First you will see the RabbitMQ process start up this can take up to 30 seconds. Thereafter, the worker is started. You should see another terminal startup. This also takes some time to startup.

Once these are up, you can head over to localhost or the server address and started uploading files.

### Clean-up
Local data is stored in `../SFCompareAndLoad/temp/`, which is created when you run the program (same as the log folder).

<p align="right">(<a href="#top">back to top</a>)</p>

## Debugging
Information to help with finding issues with the app can be found below.

### Loggers
The log config files are located in `../SFCompareAndLoad/logs/`, which is created when you run the program. The loggers are configured by load the log_config.json file in the root directory.

The loaded loggers are:
``` 
'fh1'  : ...
'fh2'  : ...
'...'  : ...
```

### Outputs
Outputs can be found at:
```

``` 
<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ROADMAP -->
## Roadmap

- [ ] Build version 1 for a single object
  - [ ] Process to choose create matching string -> ~~dynamic~~ or static/from env?
- [ ] Allow configurations for the matching string from the .env
- [ ] Create an executable/ batch file
- [ ] Add more object mappings

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

Nirav Surajlal - niravs@tecex.com

Project Link: [https://github.com/Nirav-TecEX/SFCompareAndLoad](https://github.com/Nirav-TecEX/SFCompareAndLoad)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Img Shields](https://shields.io)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[coverage.py-url]: https://pypi.org/project/coverage/
[python-coverage.py]: https://img.shields.io/badge/python-coverage.py-blue
