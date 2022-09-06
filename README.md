<div id="top"></div>

<!-- PROJECT LOGO -->
<br />
<div align="center">
  <a href="https://github.com/othneildrew/Best-README-Template">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">ABC</h3>

  <p align="center">
    MORE!
    <br />
    <a href="https://team.tecexlabs.dev/tecex-rules-system/docs/"><strong>LINKS »</strong></a>
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

ABC

<p align="right">(<a href="#top">back to top</a>)</p>



### Built With

* [![Python][python-coverage.py]][coverage.py-url]

## Installation
This app is a Django App that uses Celery to process the tasks with RabbitMQ as its messaging broker. RabbitMQ requires Erlang and the bot requires Maven and Java.

### Requirements
_Requirements_

1. Instruction 1 [https://example.com](https://example.com)
    - Running the command below should return:
        > $ java --version
        
        	> java 11.0.15.1 2022-04-22 LTS
        	> Java(TM) SE Runtime Environment 18.9 (build 11.0.15.1+2-LTS-10)
        	> Java HotSpot(TM) 64-Bit Server VM 18.9 (build 11.0.15.1+2-LTS-10, mixed mode)
	
2. Location:
    ```
    ABC/DE/F
    ```        	

<p align="right">(<a href="#top">back to top</a>)</p>

## Usage
Once the system has all of the requirements, the server can be started. Head over to the file directory "MedExServer\medex\" and run
  ```sh
	$ python manage.py runserver --noreload
  ```
This will start up the server. First you will see the RabbitMQ process start up this can take up to 30 seconds. Thereafter, the worker is started. You should see another terminal startup. This also takes some time to startup.

Once these are up, you can head over to localhost or the server address and started uploading files.

### Clean-up
User data is stored in:
```
ABC/DE/F/G
```

**If an error is thrown, the data is not cleared.**

<p align="right">(<a href="#top">back to top</a>)</p>

## Debugging
Information to help with finding issues with the app can be found below.

### Loggers
The log config files are located in the MedExServer/medex folder (log_config.json).

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

- [x] Run Newman Tests Locally
- [x] Hit the RulesEng at an endpoint with the Requests
- [x] Create a process for the tests
- [x] Process results
    - [x] Filter output and remove unnecessary information
    - [x] Store output
    - [ ] Relay information to testuser
- [ ] Add code coverage
- [ ] Integrate with local RulesEngine
- [ ] Integrate with any locally run RulesEngine
- [ ] Add scheduler to update the local excel files


<p align="right">(<a href="#top">back to top</a>)</p>

<!-- LICENSE -->
## License

Distributed under the MIT License. See `LICENSE.txt` for more information.

<p align="right">(<a href="#top">back to top</a>)</p>

## Contact

Nirav Surajlal - niravs@tecex.com

Project Link: [https://github.com/Nirav-TecEX/RulesEngineTests.git](https://github.com/Nirav-TecEX/RulesEngineTests.git)

<p align="right">(<a href="#top">back to top</a>)</p>

<!-- ACKNOWLEDGMENTS -->
## Acknowledgments

* [Img Shields](https://shields.io)

<p align="right">(<a href="#top">back to top</a>)</p>


<!-- MARKDOWN LINKS & IMAGES -->
<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[coverage.py-url]: https://pypi.org/project/coverage/
[python-coverage.py]: https://img.shields.io/badge/python-coverage.py-blue
