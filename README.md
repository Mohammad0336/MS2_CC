# Running the design portion

## How to use the program 

Open three terminals

run these commands in the first terminal
```bash
cd SOFE4630U-MS2/Design/
export BUCKET='gs://lab1-413419-bucket'
export PROJECT='lab1-413419'
python smartMeterTest.py \
  --runner DataflowRunner \
  --project $PROJECT \
  --staging_location $BUCKET/staging \
  --temp_location $BUCKET/temp \
  --input projects/$PROJECT/topics/smartMeterTopic    \
  --output projects/$PROJECT/topics/smartMeterTopicOutput \
  --region  northamerica-northeast2 \
  --experiment use_unsupported_python_version \
  --streaming
```

run these commands in the second terminal after pipeline is streaming
```bash
cd SOFE4630U-MS2/Design/
python producer.py
```

Open a terminal in the client file

run these commands in the third terminal
```bash
cd SOFE4630U-MS2/Design/
python con.py
```

You can also see the initial results in the input topic
```bash
cd SOFE4630U-MS2/Design/
python consumer.py
```
