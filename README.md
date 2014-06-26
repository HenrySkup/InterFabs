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
to be written.

###User Workflows

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

##Deeper Info
###Directory Usage
```testSite``` contains resources for init website.  nothing more, nothing less.  
```.vagrant``` do not touch  
```provision```  

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
