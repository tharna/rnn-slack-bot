Simple slack slash command backend for providing comments.

Install Serverless framework:
`npm install -g serverless`

Generate your trained model. You can run textgenrnn on your local computer: https://github.com/minimaxir/textgenrnn
But that will be slow unless you have a powerful Nvidia GPU on your machine. A better option is to use colab which provides free access to Google NPU's for limited time (around 4 hours, which is plenty to train a simple model). You can find example colab notebook from: https://github.com/minimaxir/textgenrnn/blob/cfba96c9f6baa347d1493df4be72f92b2fb3815b/docs/textgenrnn-demo.ipynb

Once you have the model place it under `model/` folder.

Build vendored libraries:
```
docker build -f Dockerfile --tag lambda:latest .
docker run --name lambda -itd lambda:latest
docker cp lambda:/tmp/vendored/ vendored
docker stop lambda
```

Copy config.yml.exaple to config.yml and add your Slack token

Make sure you have AWS cli installed and credentials set

Run `sls deploy`

Add your API endpoint to your slack slash command


