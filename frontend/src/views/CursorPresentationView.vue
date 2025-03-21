<template>
  <div class="presentation-container">
    <!-- Background cosmic elements -->
    <div class="floating-dots">
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
      <div class="dot"></div>
    </div>
    <div class="grid-lines"></div>
    <div class="planet-ring"></div>
    <div class="orbital-path"></div>
    <div class="stars">
      <div class="star" v-for="n in 80" :key="n" :style="{ 
        top: Math.random() * 100 + '%', 
        left: Math.random() * 100 + '%',
        width: (Math.random() * 2 + 1) + 'px',
        height: (Math.random() * 2 + 1) + 'px',
        animationDelay: Math.random() * 5 + 's'
      }"></div>
    </div>
    
    <div class="content-wrapper">
      <div class="slide-card">
        <div class="slide-container">
          <transition :name="transitionName">
            <component :is="slides[currentSlideIndex]" :key="currentSlideIndex"></component>
          </transition>
        </div>
        
        <div class="slide-indicator">
          <div v-for="(slide, index) in slides" :key="index" 
               :class="['indicator-dot', {'active': index === currentSlideIndex}]"
               @click="goToSlide(index)"></div>
        </div>
      </div>
    </div>
    
    <div class="controls">
      <button @click="prevSlide" :disabled="currentSlideIndex === 0" class="nav-btn prev-btn">
        <span class="btn-icon">◀</span>
        <span class="btn-text">Previous</span>
      </button>
      
      <div class="pagination">
        <span class="current-slide">{{ currentSlideIndex + 1 }}</span>
        <div class="pagination-divider"></div>
        <span class="total-slides">{{ slides.length }}</span>
      </div>
      
      <button @click="nextSlide" :disabled="currentSlideIndex === slides.length - 1" class="nav-btn next-btn">
        <span class="btn-text">Next</span>
        <span class="btn-icon">▶</span>
      </button>
    </div>
  </div>
</template>

<script>
import CursorIntroSlide from '../components/presentation/CursorIntroSlide.vue';
import CursorComparisonSlide from '../components/presentation/CursorComparisonSlide.vue';
import CursorDemoSlide from '../components/presentation/CursorDemoSlide.vue';

export default {
  name: 'CursorPresentationView',
  components: {
    CursorIntroSlide,
    CursorComparisonSlide,
    CursorDemoSlide
  },
  data() {
    return {
      currentSlideIndex: 0,
      transitionName: 'fade',
      slides: [
        'CursorIntroSlide',
        'CursorComparisonSlide',
        'CursorDemoSlide'
      ]
    }
  },
  methods: {
    nextSlide() {
      if (this.currentSlideIndex < this.slides.length - 1) {
        this.transitionName = 'zoom-out';
        this.currentSlideIndex++;
      }
    },
    prevSlide() {
      if (this.currentSlideIndex > 0) {
        this.transitionName = 'zoom-in';
        this.currentSlideIndex--;
      }
    },
    goToSlide(index) {
      if (index === this.currentSlideIndex) return;
      
      this.transitionName = index > this.currentSlideIndex ? 'zoom-out' : 'zoom-in';
      this.currentSlideIndex = index;
    },
    // Keyboard navigation
    handleKeyDown(e) {
      if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ') {
        this.nextSlide();
      } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        this.prevSlide();
      }
    }
  },
  mounted() {
    window.addEventListener('keydown', this.handleKeyDown);
  },
  beforeUnmount() {
    window.removeEventListener('keydown', this.handleKeyDown);
  }
}
</script>

<style scoped>
.presentation-container {
  display: flex;
  flex-direction: column;
  height: 100vh;
  background-color: var(--bg-body, #0a0e21);
  color: var(--text-primary, #e6e6ff);
  position: relative;
  overflow: hidden;
  z-index: 1;
}

/* Modern background elements */
.presentation-container::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-image: 
    radial-gradient(circle at 10% 20%, rgba(58, 134, 255, 0.12) 0%, transparent 50%),
    radial-gradient(circle at 90% 80%, rgba(251, 86, 7, 0.12) 0%, transparent 50%),
    radial-gradient(circle at 50% 50%, rgba(42, 157, 143, 0.08) 0%, transparent 70%);
  z-index: -1;
}

/* Planet */
.presentation-container::after {
  content: "";
  position: absolute;
  width: 220px;
  height: 220px;
  top: -40px;
  right: -30px;
  background: radial-gradient(circle, rgba(42, 157, 143, 0.5) 0%, rgba(58, 134, 255, 0.3) 60%, transparent 100%);
  border-radius: 50%;
  box-shadow: inset 20px -20px 40px rgba(255, 255, 255, 0.4),
              inset -10px 10px 30px rgba(0, 0, 40, 0.6);
  z-index: -1;
  animation: planetRotate 60s infinite linear;
  filter: blur(4px);
}

@keyframes planetRotate {
  0% {
    box-shadow: inset 20px -20px 40px rgba(255, 255, 255, 0.4),
                inset -10px 10px 30px rgba(0, 0, 40, 0.6);
  }
  50% {
    box-shadow: inset -20px 20px 40px rgba(255, 255, 255, 0.4),
                inset 10px -10px 30px rgba(0, 0, 40, 0.6);
  }
  100% {
    box-shadow: inset 20px -20px 40px rgba(255, 255, 255, 0.4),
                inset -10px 10px 30px rgba(0, 0, 40, 0.6);
  }
}

/* Planet Ring */
.planet-ring {
  position: absolute;
  top: -50px;
  right: -70px;
  width: 300px;
  height: 300px;
  border-radius: 50%;
  z-index: -1;
  overflow: visible;
  transform: rotateX(75deg) rotateY(15deg);
  pointer-events: none;
  animation: orbitRotate 80s infinite linear;
}

@keyframes orbitRotate {
  from { transform: rotateX(75deg) rotateY(15deg) rotateZ(0deg); }
  to { transform: rotateX(75deg) rotateY(15deg) rotateZ(360deg); }
}

.planet-ring::before {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 260px;
  height: 260px;
  transform: translate(-50%, -50%);
  border: 10px solid rgba(251, 186, 114, 0.2);
  border-radius: 50%;
  box-shadow: 0 0 20px rgba(251, 186, 114, 0.4);
}

.planet-ring::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  width: 220px;
  height: 220px;
  transform: translate(-50%, -50%);
  border: 6px solid rgba(58, 134, 255, 0.2);
  border-radius: 50%;
}

/* Additional ring */
.orbital-path {
  position: absolute;
  top: 25%;
  left: -15%;
  width: 150vh;
  height: 150vh;
  border: 1px dashed rgba(58, 134, 255, 0.1);
  border-radius: 50%;
  animation: orbit-rotate 150s linear infinite;
}

@keyframes orbit-rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Floating Dots */
.floating-dots {
  position: absolute;
  z-index: -1;
  pointer-events: none;
  width: 100%;
  height: 100%;
}

.floating-dots .dot {
  position: absolute;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background-color: rgba(58, 134, 255, 0.3);
  animation: float 8s infinite ease-in-out;
}

.floating-dots .dot:nth-child(1) {
  top: 15%;
  left: 10%;
  width: 4px;
  height: 4px;
  animation-delay: 0s;
  background-color: rgba(58, 134, 255, 0.3);
}

.floating-dots .dot:nth-child(2) {
  top: 25%;
  left: 20%;
  width: 8px;
  height: 8px;
  animation-delay: 1s;
  animation-duration: 10s;
  background-color: rgba(42, 157, 143, 0.3);
}

.floating-dots .dot:nth-child(3) {
  top: 60%;
  left: 5%;
  width: 6px;
  height: 6px;
  animation-delay: 2s;
  animation-duration: 7s;
  background-color: rgba(251, 86, 7, 0.3);
}

.floating-dots .dot:nth-child(4) {
  top: 70%;
  left: 80%;
  width: 5px;
  height: 5px;
  animation-delay: 3s;
  animation-duration: 9s;
  background-color: rgba(58, 134, 255, 0.3);
}

.floating-dots .dot:nth-child(5) {
  top: 40%;
  left: 85%;
  width: 7px;
  height: 7px;
  animation-delay: 4s;
  animation-duration: 8s;
  background-color: rgba(42, 157, 143, 0.3);
}

.floating-dots .dot:nth-child(6) {
  top: 30%;
  left: 60%;
  width: 4px;
  height: 4px;
  animation-delay: 2.5s;
  animation-duration: 11s;
  background-color: rgba(251, 86, 7, 0.3);
}

.floating-dots .dot:nth-child(7) {
  top: 80%;
  left: 30%;
  width: 6px;
  height: 6px;
  animation-delay: 3.5s;
  animation-duration: 9s;
  background-color: rgba(251, 86, 7, 0.3);
}

.floating-dots .dot:nth-child(8) {
  top: 15%;
  left: 70%;
  width: 5px;
  height: 5px;
  animation-delay: 4.5s;
  animation-duration: 10s;
  background-color: rgba(58, 134, 255, 0.3);
}

@keyframes float {
  0%, 100% {
    transform: translateY(0) translateX(0);
  }
  25% {
    transform: translateY(-25px) translateX(15px);
  }
  50% {
    transform: translateY(10px) translateX(-12px);
  }
  75% {
    transform: translateY(15px) translateX(8px);
  }
}

/* Stars */
.stars {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -2;
  pointer-events: none;
}

.star {
  position: absolute;
  background-color: white;
  border-radius: 50%;
  opacity: 0.4;
  animation: twinkle 4s infinite ease-in-out;
}

@keyframes twinkle {
  0%, 100% { opacity: 0.2; transform: scale(0.8); }
  50% { opacity: 0.7; transform: scale(1.2); }
}

/* Grid Lines */
.grid-lines {
  position: absolute;
  z-index: -1;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  pointer-events: none;
  opacity: 0.06;
  background-image: 
    linear-gradient(to right, var(--primary, #3a86ff) 1px, transparent 1px),
    linear-gradient(to bottom, var(--primary, #3a86ff) 1px, transparent 1px);
  background-size: 40px 40px;
  animation: grid-pulse 10s infinite ease-in-out;
}

@keyframes grid-pulse {
  0%, 100% { opacity: 0.04; }
  50% { opacity: 0.09; }
}

/* Content Wrapper */
.content-wrapper {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 2rem;
  perspective: 1000px;
}

.slide-card {
  width: 100%;
  max-width: 900px;
  background: rgba(15, 23, 42, 0.6);
  border-radius: 16px;
  backdrop-filter: blur(20px);
  border: 1px solid rgba(100, 120, 255, 0.2);
  overflow: hidden;
  box-shadow: 
    0 20px 40px rgba(0, 0, 0, 0.2),
    0 0 0 1px rgba(255, 255, 255, 0.1) inset,
    0 0 30px rgba(58, 134, 255, 0.15);
  transition: all 0.5s ease;
  position: relative;
  transform-style: preserve-3d;
  animation: cardIntro 1s ease;
}

@keyframes cardIntro {
  from {
    opacity: 0;
    transform: translateY(30px) rotateX(10deg);
  }
  to {
    opacity: 1;
    transform: translateY(0) rotateX(0deg);
  }
}

.slide-card::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent, rgba(165, 180, 252, 0.5), transparent);
  z-index: 1;
}

.slide-container {
  padding: 2rem;
  position: relative;
  min-height: 400px;
  display: flex;
  justify-content: center;
  align-items: center;
}

.slide-indicator {
  display: flex;
  justify-content: center;
  gap: 10px;
  padding: 1rem 0;
  position: relative;
}

.indicator-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.3);
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
}

.indicator-dot::after {
  content: "";
  position: absolute;
  top: -5px;
  left: -5px;
  right: -5px;
  bottom: -5px;
  border-radius: 50%;
  background-color: transparent;
  z-index: 1;
}

.indicator-dot:hover {
  background-color: rgba(255, 255, 255, 0.6);
  transform: scale(1.2);
}

.indicator-dot.active {
  background-color: rgba(58, 134, 255, 0.8);
  box-shadow: 0 0 10px rgba(58, 134, 255, 0.7);
  transform: scale(1.2);
}

/* Controls Section */
.controls {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 1.25rem 2rem;
  background-color: rgba(10, 14, 33, 0.8);
  backdrop-filter: blur(10px);
  border-top: 1px solid rgba(100, 120, 255, 0.2);
  z-index: 3;
  position: relative;
}

/* Add subtle line glow effect */
.controls::after {
  content: "";
  position: absolute;
  top: 0;
  left: 30%;
  width: 40%;
  height: 1px;
  background: linear-gradient(to right, transparent, var(--primary, #3a86ff), transparent);
  filter: blur(1px);
  animation: line-glow 4s infinite ease-in-out;
}

@keyframes line-glow {
  0%, 100% { opacity: 0.3; }
  50% { opacity: 1; }
}

.pagination {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  background: rgba(15, 23, 42, 0.5);
  padding: 0.5rem 1rem;
  border-radius: 30px;
  border: 1px solid rgba(100, 120, 255, 0.15);
  box-shadow: 0 0 15px rgba(58, 134, 255, 0.15);
}

.current-slide {
  font-size: 1.2rem;
  font-weight: 700;
  color: rgba(165, 180, 252, 1);
}

.pagination-divider {
  width: 25px;
  height: 2px;
  background: linear-gradient(to right, transparent, rgba(165, 180, 252, 0.5), transparent);
  transform: rotate(-45deg);
}

.total-slides {
  font-size: 1rem;
  color: rgba(165, 180, 252, 0.7);
}

.nav-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1.5rem;
  background: rgba(15, 23, 42, 0.5);
  color: rgba(165, 180, 252, 0.9);
  border: 1px solid rgba(100, 120, 255, 0.2);
  border-radius: 30px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-weight: 600;
  font-size: 0.95rem;
  box-shadow: 0 0 15px rgba(58, 134, 255, 0.1);
  position: relative;
  overflow: hidden;
}

.nav-btn::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: linear-gradient(135deg, rgba(100, 120, 255, 0.1), transparent);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.nav-btn:hover::before {
  opacity: 1;
}

.nav-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(58, 134, 255, 0.2);
  color: white;
  border-color: rgba(100, 120, 255, 0.4);
}

.nav-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: rgba(15, 23, 42, 0.3);
  transform: none;
  box-shadow: none;
  color: rgba(165, 180, 252, 0.5);
}

.nav-btn:disabled::before {
  display: none;
}

.btn-icon {
  font-size: 0.8rem;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Slide transitions */
.zoom-out-enter-active,
.zoom-out-leave-active,
.zoom-in-enter-active,
.zoom-in-leave-active,
.fade-enter-active,
.fade-leave-active {
  transition: all 0.5s cubic-bezier(0.4, 0.0, 0.2, 1);
}

.zoom-out-enter-from {
  opacity: 0;
  transform: scale(0.8);
}

.zoom-out-leave-to {
  opacity: 0;
  transform: scale(1.2);
}

.zoom-in-enter-from {
  opacity: 0;
  transform: scale(1.2);
}

.zoom-in-leave-to {
  opacity: 0;
  transform: scale(0.8);
}

.fade-enter-from, .fade-leave-to {
  opacity: 0;
}

/* Media queries for responsive design */
@media (max-width: 900px) {
  .content-wrapper {
    padding: 1.5rem;
  }
  
  .slide-container {
    padding: 1.5rem;
    min-height: 350px;
  }
  
  .controls {
    padding: 1rem 1.5rem;
  }
}

@media (max-width: 768px) {
  .controls {
    padding: 0.75rem 1.25rem;
  }
  
  .nav-btn {
    padding: 0.6rem 1.2rem;
    font-size: 0.9rem;
  }
  
  .btn-text {
    display: none;
  }
  
  .nav-btn {
    gap: 0;
  }
  
  .btn-icon {
    font-size: 1rem;
  }
}

@media (max-width: 480px) {
  .content-wrapper {
    padding: 1rem;
  }
  
  .slide-container {
    padding: 1rem;
    min-height: 300px;
  }
  
  .controls {
    padding: 0.6rem 1rem;
  }
  
  .pagination {
    padding: 0.35rem 0.75rem;
  }
  
  .current-slide, .total-slides {
    font-size: 1rem;
  }
  
  .pagination-divider {
    width: 20px;
  }
  
  .nav-btn {
    padding: 0.5rem;
    border-radius: 50%;
    width: 36px;
    height: 36px;
    display: flex;
    justify-content: center;
  }
}
</style> 

