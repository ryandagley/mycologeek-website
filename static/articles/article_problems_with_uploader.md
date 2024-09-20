
## How I Accidentally Turned My Raspberry Pi into a Script Factory (And How I Fixed It)

So, in my **Mycologeek** project, I recently ran into a bit of a mess with my Raspberry Pi and some sensors. The plan seemed simple enough: read some data from two sensors, upload that data to AWS S3, and feel like a coding genius.

But, as we all know, plans like that rarely go as smoothly as you’d hope.

### The Plan: Quick and Dirty Testing

I wanted to test things quickly (because who has the patience to wait?), so I set my Raspberry Pi to read sensor data and upload it to S3 **every few seconds**. The idea was to speed things up while testing. Once everything worked, I’d scale it back to something more sensible, like every 15 minutes or every hour. 

To automate the process, I set up **CRON** to run the script every 15 minutes, thinking, "Yeah, that’ll do the trick."

### The Reality: Script Gone Wild

Here’s where things started to go off the rails. My script was happily uploading data to S3 **every 3 seconds**—so far, so good, right? But CRON was also **starting a new instance of the script every 15 minutes**. So now I had a script that was *already* writing to S3 every 3 seconds, but every 15 minutes, a **brand new script** would start doing the exact same thing.

That meant I had multiple versions of the same script all running at once, each one uploading sensor data to S3 as fast as it could. Before I knew it, my poor Raspberry Pi was juggling multiple scripts, all shouting, "Upload! Upload! Upload!" 

Thankfully, my payloads were small (never more than 1MB a day), so things didn’t blow up too badly. But here’s the kicker: my Raspberry Pi **crashed**. Yep, it just couldn’t take it anymore. It was like, “Enough with the scripts already!”

### Diagnosis: Multiple Scripts Gone Rogue

At first, I wasn’t entirely sure why the Pi had given up on life, but I had a pretty good idea. To check, I ran the command:

```bash
ps aux | grep python
```

This basically says, "Show me everything that's running," and sure enough, there were **multiple instances** of my script running, all uploading to S3. It was like when Neo had to fight all the Agent Smiths.

Turns out, my script was designed to run in an infinite loop (`while True`), which means it never stopped until the Pi crashed or someone manually intervened. And since CRON was happily starting a new version every 15 minutes, I ended up with an army of scripts doing the same thing over and over again. Oops.

### The Fix: One and Done

The solution? It wasn’t hard, but it was definitely a facepalm moment. Instead of letting the script run in an infinite loop, I needed to make sure it only ran **once** per CRON trigger, uploaded the data to S3, and then stopped.

I also added a bit of logic to make sure the script would **wait for both sensors** to actually send data before uploading. I didn’t want it writing blanks to S3 just because a sensor was snoozing.

So now, here’s how it works:
1. The script runs **once** every 15 minutes, thanks to CRON.
2. It waits for both sensors to give valid data.
3. After both sensors check in, it uploads the data to S3 **and stops**.
4. Then, 15 minutes later, CRON runs it again, and the process repeats—**just once**, no clones.

### The Lesson: Don’t Let Your Scripts Run Wild

This whole experience taught me an important lesson about scripting with CRON: If you’re writing a script that’s only supposed to run once, make sure it actually stops when it’s done! Otherwise, you might end up with **dozens of rogue scripts** running simultaneously, like I did.

Also, if your Raspberry Pi crashes and you’re like, "Why?!", maybe check to see how many scripts are running. You might be surprised.

### Conclusion: My Raspberry Pi Is Now Happily Under Control

Now that I’ve fixed my script, the Raspberry Pi is back to normal. It collects sensor data every 15 minutes, uploads it to S3, and then stops. No more script armies, no more crashes, and the data is correctly reflected on my monitoring page. Mission accomplished.

So, if you’re a beginner like me, remember this: **One and done is your friend** when it comes to CRON jobs. Don’t let your scripts multiply like bunnies. Trust me, it’ll save you a lot of headaches.

---

### Final Thoughts

If you’re using CRON and your Raspberry Pi to run scripts, be careful about how long they run. Make sure they end when they’re supposed to, and use tools like `ps aux` to check if something is going haywire. Otherwise, you might end up with a lot more happening than you bargained for!


