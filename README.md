# WebScienceCourseWork
Web science course work.
## How to Run
1. Download the MongoDB file from [https://github.com/helloqiu/WebScienceCourseWork/releases/download/1.0/mongo_sample.tar.gz](https://github.com/helloqiu/WebScienceCourseWork/releases/download/1.0/mongo_sample.tar.gz).  
Extract it by command:

``` bash
tar -xzf mongo_sample.tar.gz
```  

2. Install `Docker` and `docker-compose` and run
``` bash
docker-compose up -d
```
to start the MongoDB Server. There is also a MongoExpress server running and you can check it out by visiting [http://localhost:8081/](http://localhost:8081/).  
The username for the DB is `root` and the password is `example`.

3. Install dependencies
``` bash
pip install -r requirements.txt
```
Please run it with `Python 3.8.2`.

4. Create `config.json`

``` json
{
    "consumer_key": "",
    "consumer_secret": "",
    "access_token_key": "",
    "access_token_secret": "",
    "mongo_host": "127.0.0.1",
    "mongo_username": "root",
    "mongo_password": "example"
}
```
Fill `consumer_key`, `consumer_secret`, `access_token_key`, `access_token_secret` with your own.

5. Run crawler
``` bash
python crawler.py [emotion]
```
Replace `[emotion]` with the emotion class e.g. happy or angry.

6. Run pre-processing
``` bash
python pre_process.py
```

7. Run categorizing
``` bash
python categorize.py
```

## Data
`crowdsourcing_input.csv` contains the data for crowdsourcing.  
`cf_report_1556720_full.csv` contains the data returned by Figure Eight.
