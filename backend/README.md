# BuzzBoard 
Where Conversations Come to Life!

## Introduction
<img src="./img/logo.png" align="right"
     alt="Size Limit logo" width="120" height="178">


BuzzBoard is an application that aims to create a space where people around the world can come together to discuss and share their thoughts on a variety of different topics like books, games, music, and news.

* **Project Page**: [BuzzBoard](http://web-02.akt-global.tech/)
* **Blog Post**: 

### Authors
* Ato Kwamena Toffah [Github](https://github.com/UnfetteredScholar) | [Linkedin](https://www.linkedin.com/in/ato-k-toffah/)

* Jessica Asamoah [Github](https://github.com/Jessica-Asamoah) | [Linkedin](https://www.linkedin.com/in/jessica-awuradjoa-asamoah-402ba6191/)


## Installation

### Backend - Docker
* Edit environment variables and run the docker compose provided.

### Backend
**Required**
1. Mongodb
2. Poetry
3. Python version 3.11 

**Process**
* Install project requirements using poetry (**poetry install**)
* Set the following environment variables:
1. SECRET_KEY=(RUN: openssl rand -hex 32)
2. ALGORITHM=HS256
3. ACCESS_TOKEN_EXPIRE_DAYS=
4. RESET_PASSWORD_URL=
5. VERIFY_EMAIL_URL=
6. EMAIL_ACCOUNT=
7. EMAIL_PASSWORD=
8. SMTP_HOST=
9. SMTP_PORT=
10. MONGO_URI=

* Run server with: **uvicorn main:app --host 0.0.0.0**

### Frontend
1. RUN: npm install vite
2. RUN: npm run build
3. Serve static files with the program of your choice


## Usage

* Follow the instructions above to setup the project
* Access the web app through your browser


## Related projects

* [IReader](https://github.com/IReaderorg/IReader)
* [Lnreader](https://github.com/LNReader/lnreader)
* [WNReader](https://github.com/Nithin-Johnson/WNReader)