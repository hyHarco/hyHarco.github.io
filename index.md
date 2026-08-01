---
title: Home
layout: default
---

<!-- Swiper CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@10.3.1/swiper-bundle.min.css" />


<section class="home_hero">
  <div class="swiper mySwiper">
    <div class="swiper-wrapper">
      <div class="swiper-slide"><img src="/images/main_img/1.png" alt="HARCO Lab" fetchpriority="high" decoding="async"></div>
      <div class="swiper-slide cover"><img src="/images/main_img/2.jpg" alt="HARCO Lab" loading="lazy" decoding="async"></div>
      <div class="swiper-slide"><img src="/images/main_img/3.png" alt="HARCO Lab" loading="lazy" decoding="async"></div>
      <div class="swiper-slide"><img src="/images/main_img/4.jpg" alt="HARCO Lab" loading="lazy" decoding="async"></div>
    </div>
    <div class="swiper-button-next"></div>
    <div class="swiper-button-prev"></div>
    <div class="swiper-pagination"></div>
  </div>
</section>

<div class="home_intro">
  <div class="home_intro_logo">
    <img src="/images/common/harco.png" alt="HARCO Lab" loading="lazy" decoding="async" />
  </div>

  <div class="home_intro_text">
    <h1 class="home_title">Hum<b>A</b>n-<b>R</b>obot <b>CO</b>llaboration Research Lab</h1>

    <p class="home_lead">
    We study how humans and robots can work together — physically, cognitively, and reliably. Our research spans Physical Human-Robot Interaction (pHRI), shared and whole-body control, ergonomics and human factors, haptic and tactile sensing, machine learning for robotics, and powered exoskeletons.
    </p>
  </div>
</div>

<div class="home_cta">Interested in joining the lab? Send your CV to <a href="mailto:wansookim+app@hanyang.ac.kr">wansookim+app@hanyang.ac.kr</a>.</div>

{% include home-topics-strip.html %}

{% include home-news-strip.html %}

{% include home-youtube-strip.html %}

<!-- Swiper JS -->
<script src="https://cdn.jsdelivr.net/npm/swiper@10.3.1/swiper-bundle.min.js" defer></script>
<script src="{{ '/js/home-hero.js' | relative_url }}" defer></script>
