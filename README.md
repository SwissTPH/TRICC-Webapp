# tricc_webapp
Web application to convert drawio workflow diagrams into XForm data using TRICC.

![TRICC_Interface](tricc_interface.png)

### Software
- Streamlit
- Python
- Docker
- TRICC

### Prerequisites
- Docker

### Configuration
**Users** \
The config.yaml file holds the information of users with access to the application, to allow a user to register, they have to be placed under _preauthorized_.

**Docker** \
There is a Dockerfile as well as a docker-compose.yml configuration for easy set-up which automatically installs all requirements.

**TRICC** \
Everything related to TRICC is stored separately in the _TRICC/_ folder which contains it's own requirements.

### Reference files
There are references files stored in the directory _reference_files_ as an example on valid data to be uploaded and used with the app.

### How to run
1. Clone the project
2. _cd_ into the cloned project
3. Make sure that Docker is running and execute following command:

```
docker-compose up -d
```
4. Navigate to the URL shown in the terminal
By default it will be:

```
http://localhost:8501
```


**Credits**
- App by [Patrick Meier](https://www.swisstph.ch/en/people-teaser-detail/teaser-detail/patrick-meier#pageRecord)
- TRICC by [Rafael Kluender](https://www.swisstph.ch/en/people-teaser-detail/teaser-detail/rafael-kluender#pageRecord)
