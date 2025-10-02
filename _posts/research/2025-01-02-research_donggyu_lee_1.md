---
title: Proactive Ergonomic Human Motion Generation for Human-Robot Collaboration
image: images/research/donggyu_main.png
tags:
  - human-robot collaboration
  - ergonomics
  - human-centric control
  - proactive safety

author: Donggyu-Lee
member: Donggyu-Lee
group: research_1
---
**Goal** :  To predict human ergonomic states and generate ergonomic human motion to reduce the risk of work-related musculoskeletal disorders (WMSDs).

***

**Summary**
This study presents a human-centric, proactive ergonomic safety framework for human-robot collaboration (HRC), designed to ensure that human motion remains physically safe and ergonomically compliant during collaborative tasks.A vector auto-regressive (VAR) model is used to predict short-term human joint trajectories based on repetitive task data, and the predicted motion is tracked by a virtual human model.Control Barrier Functions (CBFs) are employed to enforce ergonomic constraints in real time, including stance stability via the Center of Pressure (CoP) and effort alignment through the force manipulability ellipsoid.Simulations of collaborative lifting tasks demonstrate that the proposed framework effectively keeps the predicted motion within the ergonomic safety set.Quantitative results show a 24.6% reduction in average overloading joint torque at the shoulder and a decrease in total biomechanical effort by 48.1% and 60.8% at the shoulder and elbow, respectively.These reductions highlight the potential of the proposed approach to enable robot systems that proactively adapt to human motion while ensuring ergonomic safety in physically interactive tasks.

***

{%
  include figure.html
  image="images/research/donggyu_1.png"
%}
