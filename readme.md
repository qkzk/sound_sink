# Sound Sink

Change your sound sink from command line easily.

It uses `pacmd` to get the available sound sinks.
With `grep` we filter the output to get the names and indexes.
Then we change the sound sink to the desired one.

```bash
$ sound_sink corsair
```

If you have a `corsair` headset.

```bash
$ sound_sink analog
```

For analog sound sink.
