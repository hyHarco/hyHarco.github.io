---
title: Home
layout: default
---

<!-- HARCO 로고 -->
<h1 class="animate__animated animate__fadeIn">
  <img src="images/harc.png" loading="lazy" style="width: 60%" />
</h1>

<!-- Swiper CSS -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.css" />

<style>
  .mySwiper {
    width: 100%;
    margin: 30px 0;
    aspect-ratio: 16 / 9;  /* 원하는 비율로 고정 */
    max-height: 70vh;      /* 너무 높아지지 않게 상한 */
    min-height: 280px;     /* 너무 낮아지지 않게 하한 */
    overflow: hidden;
    min-height: 0;
  }
  .mySwiper .swiper-slide img {
    width: 100%;
    height: 100%;
    object-fit: cover;    /* 꽉 채우기(잘림 감수) */
    display: block;
  }
</style>

<div class="swiper mySwiper">
  <div class="swiper-wrapper">
    <div class="swiper-slide"><img src="/images/lab_2.png" alt="lab_2"></div>
    <div class="swiper-slide"><img src="/images/lab_1.png" alt="lab_1"></div>
    <div class="swiper-slide"><img src="/images/lab_3.png" alt="lab_3"></div>
  </div>

  <!-- 화살표 -->
  <div class="swiper-button-next"></div>
  <div class="swiper-button-prev"></div>
  <!-- 페이지네이션 -->
  <div class="swiper-pagination"></div>
</div>

<!-- Swiper JS -->
<script src="https://cdn.jsdelivr.net/npm/swiper@10/swiper-bundle.min.js"></script>
<script>
  const swiper = new Swiper(".mySwiper", {
    loop: true,
    pagination: { el: ".swiper-pagination", clickable: true },
    navigation: { nextEl: ".swiper-button-next", prevEl: ".swiper-button-prev" },
  });
</script>

<!-- 소개 문구 -->
<div class="animate__animated animate__fadeInDown" style="font-size: 19px; text-align:left">
Welcome to the <b>HumAn-Robot COllaboration (HARCO)</b> Research Lab! <br>
Our research interests include Physical Human-Robot Interaction (pHRI), Human-Robot Collaboration, Shared Control, Whole-body Control, Ergonomics, Human Factor Engineering, Haptic and Tactile sensing, Machine Learning for Robotics and Powered Exoskeleton Robots.
<br><br>
</div>

<div class="animate__animated animate__fadeInDown" style="font-size: 19px; text-align:left">
If you are interested in joining our team, please send your CV to:
<a href='mailto:wansookim@hanyang.ac.kr'>wansookim@hanyang.ac.kr</a>
</div>