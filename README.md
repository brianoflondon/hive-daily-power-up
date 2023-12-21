# hive-daily-power-up
Power up a Hive account every day

`git clone https://github.com/brianoflondon/hive-daily-power-up.git`

Edit the file `sample.env` and rename it `.env`. You do need your active key for power ups.

You need Docker then all you need to do is use docker:

`docker compose up -d`

It will try to power up the amount sent every day, checking every 8 hours.
