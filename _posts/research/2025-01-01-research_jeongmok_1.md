---
title: Real-Time Classification of Intentional and Unintentional Physical Contacts Using Joint Torque Patterns in Robot Manipulation


image: images/research/jeongmok_main.png
tags:
  - Contact Classification
  - Human Robot Interaction(HRI)
  - Real-Time Robot Perception 
author: Jeongmok-Kim
member: Jeongmok-Kim
group: research_2
---
**Goal** : To develop a real-time classification system that can distinguish between intentional physical interactions and unintentional collisions during robot manipulation, enabling safer and more intelligent human-robot collaboration.


***

**Summary**
This study proposes a contact classification framework that leverages joint-level torque information to differentiate between intentional interactions and unexpected collisions. Using joint position, velocity, effort, and estimated external torque, the system extracts temporal error-based features over short windows (e.g., 200 ms) and classifies contact types using a bagged tree model trained on labeled data. A rule-based trigger mechanism is integrated to stabilize contact states by monitoring the persistence of external torque errors—transitions to non-contact or intent states occur only after 1 second of inactivity, ensuring robust classification even during borderline or transient interactions. The framework is implemented in a low-latency ROS environment and logs predictions alongside torque behaviors, enabling real-time monitoring and post-analysis. Results show high responsiveness and reliability in distinguishing subtle contact differences during human-guided tasks and unexpected physical contacts.
***

{% capture col1 %}
{%
  include figure.html
  image="images/research/jeongmok_1.png"
  caption="Contact Classification(Green:non-contact, Blue:intent-contact, Red:collision)"
%}
{% endcapture %}
{% capture col2 %}
{%
  include figure.html
  image="images/research/jeongmok_2.png"
  caption="Trigger Contact State"
%}
{% endcapture %}
{% include two-col.html col1=col1 col2=col2 %}