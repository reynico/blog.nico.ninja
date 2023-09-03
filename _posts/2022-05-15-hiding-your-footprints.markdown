---
layout: post
title: "Hiding your footprints"
date: 2022-05-15 15:05:00 -0300
tags: [Security, Internet]
description: A neverending journey on hiding our digital footprint from the Internet.
---

![social media harms](/assets/images/hiding-1/social-media-harms.jpg)

It’s been a time since I started to focus more on security, I’ve learned about threat modeling and also about privacy and I’m not talking about what your phone listens to and crafts ads for your interests but the things you (or someone else!) deliberately exposed to the Internet.

If you're in the mid-'30s you've probably been digging into forums, BBSs, mailing lists, Reddit, Twitter, Facebook, Instagram, Picasa, Youtube, Vimeo, and a very long list of etceteras. Aware or not, you've written hundreds (if not thousands) of comments with lots of information, personal thoughts, and political-aided comments, and you've uploaded pictures and videos of you, your friends or family, your things, your projects, your travels. There's something special about posting stuff on Internet, it's that dopamine shot that we receive when a completely Internet strange likes our content.

Nowadays the cancel culture is on fire, it's just a matter of time for someone to bring up that old, politically incorrect tweet you made 10 years ago to be completely canceled.

Let's dive into a journey to remove our digital footprint from the Internet, but don't get me wrong! I'm super confident that everything posted on the Internet lives forever, but let's give it a try, at least, to hide some of our history back there (-:

- [Reconnaissance](#reconnaissance)
  - [Email addresses](#email-addresses)
  - [Usernames](#usernames)
  - [National identity number, or ID](#national-identity-number-or-id)
  - [Social networks](#social-networks)
- [Clean the mess!](#clean-the-mess)
  - [Email addresses](#email-addresses-1)
  - [Usernames or handles](#usernames-or-handles)
  - [Personal data on websites](#personal-data-on-websites)
  - [Social networks](#social-networks-1)
    - [Reddit](#reddit)
    - [Twitter](#twitter)
    - [Youtube and Vimeo](#youtube-and-vimeo)
    - [Facebook](#facebook)
    - [Instagram](#instagram)
  - [Internet forums](#internet-forums)
  - [Multimedia](#multimedia)
- [Additional resources](#additional-resources)

---

# Reconnaissance

> military observation of a region to locate an enemy or ascertain strategic features.

The very first step is to do reconnaissance and find your footprints. This includes your email addresses, usernames, pictures, videos, and comments.

## Email addresses

Let's start with an easy one: your email address(es). Just write down in Google every email address you've used in the last 20 years, quote-enclosed, please.
![email results](/assets/images/hiding-1/email-results.png)
_39 results, damn._

## Usernames

If you're old school enough, you surely choose a Nickname, an identity for the Internet. Your identity for IRC chat rooms, for your ICQ status, and for the forums and mailing lists where you spent years of your life.

Now think about it: most of these services you consumed are publicly available. Give it a try, remember any of your old-school nicknames? Put it quote-enclosed in Google and pick search.

![nickname results](/assets/images/hiding-1/nickname-results.png)
_835 results, geez._

## National identity number, or ID

Depending on your country's rules and how they manage their citizens' data, you may find interesting things about you, like where you live (or lived before!), how much do you earn (in a range), and if those rules don't extend to any other institutions, like a university, you could even find the scores of some exam you took time ago.

I found a PDF file from my university where I studied my career, funny that it's a 2009 document with complete names, IDs, and the exam scores we made on introduction to programming. A 13-year-old (and counting) document with so much personal data. Disgusting.

Angry enough? Someone uploaded several PDF files with tax information about a lot of people (including me!), and guess what? There's no way to contact the person who uploaded those files. We'll try to contact Scribd to take down that document in a while.

![nickname results](/assets/images/hiding-1/personal-data-scribd.png)
_Lots of PDF files with tax information. 46 pages on each document. Shit._

## Social networks

Ah, the juicy one. Reconnaissance here is quite easy: Just list the social networks you use or used in the past. Think about forums and mailing lists as social networks, it will ease the work. This is my list:

- Facebook
- Instagram
- Twitter
- Youtube
- Vimeo
- Reddit
- Internet forums (not listing any, in particular, the mileage may vary)

Remember that we're not trying to hide from Google or Facebook. Rather than that, it's just a matter of hiding what anyone can find about our person on the Internet.

# Clean the mess!

Well, it's time to put our hands down on the problem. Take this as a list of advice, it may not fit your needs or concerns!

## Email addresses

- Create a new email account and use a pseudonym for the handle! An email address like `john.bennet@protonmail.com` should suffice, unless you are John Bennet, right?
- Use the `+` operator when inputting your email addresses on sites you know they'll spam you. Ex: `john.bennet+ads@protonmail.com`. That way, you could setup email filters and do actions over them, for example, mark them as read or skip the inbox immediately.
  ![Protonmail filters](/assets/images/hiding-1/protonmail-filters.png)
  _Protonmail offers a simple filtering solution based on email' fields_
- Do not set a profile picture or an email signature. Trust me, no one cares about that.
- Do not create an email address for each service you want to register to, rather that, use the `+` operator to filter out emails later. If you want to sign up on Twitter, use `john.bennet+twitter@protonmail.com`. That way you centralize all your emails in a single account, but with easy discoverability.

## Usernames or handles

- Try to use as many pseudonyms as you can. During account creation, Reddit offers auto-generated usernames you can pick, and by using a password manager like [LastPass](https://www.lastpass.com/) or [1Password](https://1password.com/) you don't even need to remember what's your username for that specific website! Think about that approach for each new account you create.
- Care about what you post on the Internet. Remember: Things on the Internet live forever, even if you delete them. Ideally, you just want to post zero messages on the Internet.

## Personal data on websites

This is mostly related to the [National identity number, or ID](#national-identity-number-or-id) section. Websites that stores data from users or people are obligated to delete personal information if you ask them to do so.

- Scribd has a [report infringements page](https://support.scribd.com/hc/en-us/articles/210129146) where you can ask them to delete documents that contain personal information. I've asked them to take down some documents containing my National Identity Number (among other National Identity Numbers!). It took less than 24 hours for the document to be removed. Nice.

![Scribd report](/assets/images/hiding-1/scribd-report.png)
_Thank you, Delaney!_

- If you happen to find some personal data on any state-owned website, you could always email them, kindly asking to remove those documents where personal data is shown.
- Sometimes after successful data deletion requests, your data may still be cached by Google. Google has a [removal request form](https://support.google.com/websearch/answer/6349986) for outdated content including websites and images.

## Social networks

This section aims mostly to delete data posted on your behalf.

### Reddit
[Shreddit](https://github.com/x89/Shreddit) is a great tool to remove your footprints on Reddit. It first edits the comment or post and replaces their content with [lorem ipsum](https://loremipsum.io/) data, then deletes the entry. If you directly delete the entry it'll just show the user as `[Deleted]` but the content will stay there. Not good. [Shreddit](https://github.com/x89/Shreddit) needs you to [create an app](https://www.reddit.com/prefs/apps/) (AKA an API key) on Reddit.

### Twitter
Twitter has several data points from us: tweets, retweets, and likes.
- **Deleting Twitter likes:** Go to your profile likes tab, i.e. `https://twitter.com/reynico/likes`, fire up a developers console and paste the following Javascript snippet:

```javascript
setInterval(() => {
  document.querySelectorAll('div[data-testid="unlike"]')[0].click();
  window.scrollTo(0, window.pageYOffset + 300);
}, 1000);
```

- **Deleting Twitter tweets:**
1. Create an app on your [Twitter developer's portal](https://developer.twitter.com/en/apps) and setup a new application. Note `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_TOKEN` and `TWITTER_ACCESS_TOKEN_SECRET`.
2. Ask for your [Twitter archive](https://twitter.com/settings/your_twitter_data). You'll receive an email with a downloadable .zip file containing your Twitter archive.
3. Install [koenrh/delete-tweets](https://github.com/koenrh/delete-tweets) using pip: `python3 -m pip install delete-tweets`.
4. Run it against your `tweet.js` archive: `delete-tweets --until 2022-05-20 tweet.js`

### Youtube and Vimeo
- I have A LOT of videos uploaded on Youtube and Vimeo, some of them have over 14 years old! This is something that I refuse to delete or lose so I recommend you set their visibility to **private**. That way you'll always have access to them.

### Facebook
I haven't found any way to quickly set the visibility of my photos to hidden, so I took the (very long) time to set each photo album to private.

Profile pictures album cannot be set to private so you'll need to either delete your old profile pictures or set their privacy settings one by one.

There are some additional tasks you could benefit from: [Privacy checkup](https://www.facebook.com/privacy/checkup/?source=settings_and_privacy) is a section aimed to change the visibility of your past and future posts as well as the profile information you set.

1. Under **Who can see what you share** there's a quick form where you can review your profile information settings (set everything to "Only Me"), and on the next page you'll see "Limit past posts". Tap on "Limit" and confirm. That way your past posts will be hidden.
2. **Your data settings on Facebook** is really scary: During the time you probably accepted some Facebook permissions on several apps such as Spotify and so on. Review them in this section and delete the unused ones. You never know how much data those apps are getting from you!

### Instagram
I'd suggest setting your personal Instagram account to private. There's no reason other than exposing a big amount of the data open-wide to the Internet! Under Settings > Privacy:
  1. Set your account to private.
  2. Allow mentions just from people you follow.
  3. Under message controls, set everything to "requests" so in case someone contacts you, you'll get those messages in a different folder.

## Internet forums

Not much to do here, other than manually deleting posts or the whole account, but be careful with that! Most of the forum engines like vBulletin or phpBB keep the forum messages and just delete the username. So you'll be exposed either way, not by your username but by the content you posted.

This is a surgery-like operation as most of the forums (probably none, zero) don't provide an API to make programmatic operations over them, so you either manually delete each comment from the forums or you code a Javascript solution to be run on the developer's console.

## Multimedia
Last but not least! It's been a time since mobile phones were built with incredible cameras on them. In a way, they seemed to be a camera with a phone! Every picture and video you take with your shiny iPhone or Android mobile phone has extra metadata attached, such as camera settings and location information with very high precision.

![Picture metadata](/assets/images/hiding-1/picture-metadata.png)
_Picture metadata from an iPhone_

[Imagemagick's convert](https://imagemagick.org/script/convert.php) has a `-strip` flag to remove EXIF data from a picture, which also converts HEIC pictures to JPG for compatibility matters:
```bash
convert IMG_7773.heic -strip IMG_7773.heic.jpg
```

In case you wanted to do a bulk convert:
```bash
for f in $(ls *.heic); convert $f -strip $f.jpg;
```


# Additional resources

Hope you enjoyed our trip trying to clean up some footprints along with the Internet! It's not an easy task, but you can do a lot about your privacy in your spare time. Here are some resources to learn more about privacy:

- [r/privacy](https://www.reddit.com/r/privacy/)
- [r/opsec](https://www.reddit.com/r/opsec/)
- [hacker opsec](https://grugq.github.io/blog/categories/opsec/)

---

Happy hacking!
