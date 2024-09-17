# Moving My Flask Website from HTTP to HTTPS: A Reflection
22222222222222222222222222222222222222222222222222222222222222
When I started building my website, I didn’t think much about HTTPS. I knew it was something I should probably do, but I didn’t fully understand why. A few years ago, I noticed that browsers were starting to warn users about sites that didn’t use HTTPS, but I brushed it off for a while. After all, my site wasn’t collecting any sensitive information, so it didn’t seem like a big deal.

That changed when I saw the dreaded "Not Secure" warning pop up on my own site. Even though nothing harmful was happening, it still felt like an aesthetic issue. The idea that visitors might be uncomfortable or worried about the safety of my site started bothering me, so I decided to make the switch. It was more about the overall experience and perception of security, even if I wasn’t dealing with sensitive data.

I’ve gone through this process for most of my sites now. I didn’t like the idea of visitors feeling unsettled, so I made sure to transition everything to HTTPS. It wasn’t just about avoiding the warning labels; it was about creating a sense of trust and calm. For anyone interested, I’ve actually written a tutorial on the topic here: [Migrating from HTTP to HTTPS on AWS](https://www.dagleyblog.com/migrating-from-http-to-https-on-aws/).

## Why I Migrated

This time, the focus was on my Flask site, which I’ve hosted and deployed using AWS Elastic Beanstalk, with Route 53 handling DNS. I set it up to use HTTPS through **AWS CloudFront**. Although I wasn't collecting any user data, I just didn’t like the idea of my site looking insecure to visitors. The "Not Secure" label is enough to make anyone hesitate, and I didn’t want that.

Beyond the aesthetic concerns, I’ve come to appreciate what HTTPS actually provides:

1. **Encryption**: I don’t handle sensitive data, but HTTPS encrypts any communication between the user and the site. It’s like putting a seal on the information being passed back and forth—whether that’s just browsing content or something more interactive.
   
2. **Trust**: It’s weird how much we’ve come to rely on visual cues for trust online, but it’s real. That little padlock next to the URL puts people at ease, and I wanted to make sure that my site wasn’t making anyone feel uneasy.
   
3. **SEO**: While it’s not a huge factor for me, it’s still worth noting that Google ranks HTTPS sites higher. Over time, this adds up, and if I ever want more visibility for my site, it’ll be in a better position with HTTPS in place.

## Setting Up HTTPS with CloudFront

I used **AWS CloudFront** for my HTTPS setup. CloudFront is a content delivery network (CDN) that helps serve my website’s content quickly and securely by caching it at edge locations all over the world.

Some of the benefits I noticed using CloudFront:

- **Faster Load Times**: CloudFront caches content, which speeds up load times for visitors no matter where they are. This was a nice bonus, as performance improvements are always welcome.
- **Simplified SSL**: CloudFront has built-in support for SSL certificates, so setting up HTTPS was pretty seamless. I didn’t have to dig deep into managing the SSL certs myself.
- **Better Security**: Since CloudFront handles traffic, it adds a layer of security by blocking malicious traffic and providing protection against DDoS attacks. That’s not something I initially thought about, but I’m glad to have it in place now.

### The CloudFront Quirk: Invalidation

One thing I didn’t expect was the extra step involved when making updates to my site. Because CloudFront caches content at edge locations, whenever I make a change and push it through my **CI/CD pipeline**, the updates aren’t immediately visible on the live site. I have to manually create a **CloudFront invalidation** to tell it to refresh the cached content.

This isn’t directly related to HTTPS, but it’s part of the process now. It’s just something I’ve gotten used to as part of managing the site. I know the cache improves performance for visitors, but when I push an update, there’s that extra step to make sure the changes go live.

## Final Thoughts

Switching to HTTPS wasn’t as intimidating as I thought it might be, but I learned a lot along the way. Now, with HTTPS and CloudFront in place, I’m providing a more secure and reliable experience for visitors. It’s a small thing, but it makes me feel better about how my site is presented. The whole process also forced me to think more about security and performance, which is something I hadn’t fully considered when I first built the site.

Looking back, I’m glad I took the time to figure this out, even if it was mostly driven by the aesthetic of not wanting my site to look “insecure.” It’s been a good learning experience, and now that I’ve got the workflow down, future projects should be even smoother.
