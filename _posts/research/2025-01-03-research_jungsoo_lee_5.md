---
title: An Efficient Robot Control Framework Using the Model Context Protocol
image: images/research/jungsoo_5_main.png
tags:
  - Robot Intelligence
  - Artificial Intelligence Application System
  - Model Context Protocol
  
author: Jungsoo-Lee
member: Jungsoo-Lee
group: research_3

---
**Goal** 
The objective of this study is to propose an efficient and generalizable robot control framework that transforms natural language commands into structured MCP messages, enabling clear, consistent, and scalable control across diverse robot platforms.
 
 
***

**Summary**

This study presents an efficient and generalizable robot control framework based on the Model Context Protocol (MCP), which leverages a large language model (LLM) to interpret user-issued natural language commands and convert them into structured MCP messages. These messages are then transformed into ROS instructions by the MCP server in real time, allowing the robot to execute context-aware and consistent behaviors while maintaining a clear separation from low-level control mechanisms.
To validate the effectiveness of the proposed framework, simulation experiments were conducted using the MOCA mobile manipulator in the NVIDIA Isaac Sim environment. The robot was tasked with navigating around obstacles and returning to its original position based on natural language commands. The system achieved a 93.33% success rate across 15 trials conducted by three different users, demonstrating high reliability, accuracy, and the potential for real-world application. This framework offers a scalable and adaptable solution for natural language-driven robot control across diverse platforms.
 

***
<!-- 
**Publication Link** : 
[**2024 24th International Conference on Control, Automation and Systems (ICCAS)**](https://scholar.google.com/citations?view_op=view_citation&hl=ko&user=o7u_E8wAAAAJ&pagesize=100&citation_for_view=o7u_E8wAAAAJ:D_sINldO8mEC) -->

{% capture col1 %}
{%
  include figure.html
  image="images/research/jungsoo_5_1.png"
  
%}
{% endcapture %}
{% capture col2 %}
{%
  include figure.html
  image="images/research/jungsoo_5_2.png"
  
%}
{% endcapture %}
{% include two-col.html col1=col1 col2=col2 %}


{%
  include figure.html
  image="images/research/jungsoo_5_3.png"
  
%}