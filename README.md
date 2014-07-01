#InterFabs

Explorations in Browser-Based Applications for FabLabs

*Main site to come soon.*

----

##How to Start Developing Now :space_invader:

###Make this platform better

To be written.

###Development patterns for other platforms
It would be awesome to have a iPhone app, an Android app, a plugin for the obscure browser that you are using... but we need you help.

Please see ```devPatterns.md``` for the methodology which will have to be followed regardless of platform.  This will not only allow for you to learn for our ~~mistakes~~ trials as well as to uniform development across all platforms.

----

##About

###Introduction
to be written.

###Goals

*platform parts*

- Browser-based CAD
- Browser-based CAM (ie. tool-path computing)
- Browser-based Machine controle

*process (and indicators of success)*

- Browser-centric :: low bar-or-entry, everyone has it, os agnostic etc.
- Run with or without concurrent internet access
- Littlest/Simplest install possible (none, ideally)
- Open-Source
- HTML5 & Javascript based
- Ease of user customization via as many programming languages as is possible (ie. custom tool-path generation scripts, custom g-code/machine code generation scripts, etc.)

*If a three-year-old can use it, and if en engineer wants to use it: we have done out job.*

###Key Points & Theorems

To date, the creation of any object or *thing* is molded -- for good and for bad -- by certain workflows or *toolchains*.  In our current age of computer based design and fabrication this process is dominated by CAD and CAM; each environment requires, at least, one unique base file formats, with several other supporting files.  This layering can cause much confusion as files, user environments, settings, etc all change at alarmingly high rates.  Additionally, these tools (CAD and CAM) are large, faceless programs very difficult to learn *and* master, and often heavily dictate one design style or methodology.

Now is a time to break this paradigm or old.  We want to simplify this design procss by throwing away the unnecessary and getting out of each user's way, while giving more control to the end user to customize their own experience.

####User Workflows

```

*Current Work Flow*            *Eventual Workflow*

PreDigitalWork                    PreDigitalWork
    ||                                  ||
[via work/HCI]                          ||
    ||                            [via work/HCI]
    \/                                  ||
   CAD                                  ||
    ||                                  \/
[.stl, .3dm, etc.]                Browser CAD/CAM
    ||                                  ||
    \/                                  ||
   CAM                                  ||
    ||                            [motor controle]
[.gCode, .nc]                           ||
    ||                                  ||
    \/                                  \/
Machine                            Machine/moters
(internal driver logic)
```
####The Web Browser

Think of the application that is on nearly every device, every OS, and is used by just about every computer user.  This would be the web browser.  (And, increasingly within this category, this has been the Google Chrome browser.)  The web browser is an app accessible to anyone and everyone -- it has ease-of-use, it is free, it ise used to communicate, socialize, shop, learn, etc. -- it is familiar.  This is the key.  For a tool to be used (and loved) it has to be familiar, and there is no other app so familiar to so many different people.

On top of this human-centirc consideration, as browsers have developed and webstandards have solidified, they have become technologically advanced applications that can now do so much more than render text in semi-predicable ways.  Now they can compute things themselves, communicate with lots of different sources -- both local and non-local.  Browsers have legions ofdevelopers all around the world not only because of the economic incentives that the skill offers but because web development is highly accessible and, as stated before, robust.

As websites have become web-apps, it has been noticed that the ability to continulally (or at the very least highly regularly) communicate with central repositories is very advantageous.  Apps now only have to be downloaded and installed with two mouse clicks as opposed to the endless installs of the Sims which lasted *hours* and *hours* and required *so* many clearances and forms (and of course your parents we **never** there to do it). Also, web-apps are continually updated, they are never out-of-date (as long as they have a good team of developers and users behind them).  Adobe, Autodesk, and many other major software firms have noticed this fact and are currently transitioning to web-based (or web-enabled) platforms.

Because of this, we have decided to use the web-browser -- specifically, Google Chrome -- as the container for this project.  Because we have committed to a web-app, we then have also committed to ```JavaScript``` being the base language and logical framework.

##Deeper Info
###Directory Usage
```testSite``` contains resources for init website.  nothing more, nothing less.  
```.vagrant``` do not touch  
```provision``` developer

----

###Credits, et al.

This project is a group effort, of course, but its development is centered out of FabLab CEPT (Ahmedabad, GJ, India).  We *really* want to encurage anyone, anywhere to join the team.

####Core Team

- [Henry Skupniewicz](mailto: henryskup@gmail.com) is the head of FabLab CEPT and design thinker; he is also a visiting faculty member at CEPT University and team member of the Motwani Jadeja Family Foundation.
- [Kishan Thobhani](mailto: thobhanikishan@gmail.com>) is a web-developer extrodinare focusing on the stuff you *see*.
- [Sohil Patel](mailto: sohilpatel4932@gmail.com) is a serial entrepreneur and crazy hacker; he is also a team member of the Motwani Jadeja Family Foundation.
- [Vibhav Srivastava](mailto: vibahv2211@gmail.com) is a IIIT-H student and is interested in social conscious tech solutions.

####Thanks
This project is indebted to the following for their various forms of support.
- The Motwani Jadeja Family Foundation
- CEPT University
- MIT
- The FabFoundation
