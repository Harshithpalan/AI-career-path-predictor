// Load all interactive components
// This script is loaded via script tag to avoid module issues

// Animated Background
class AnimatedBackground {
  constructor() {
    this.canvas = null;
    this.ctx = null;
    this.particles = [];
    this.mouse = { x: 0, y: 0 };
    this.init();
  }

  init() {
    this.createCanvas();
    this.createParticles();
    this.setupEventListeners();
    this.animate();
  }

  createCanvas() {
    this.canvas = document.createElement('canvas');
    this.canvas.id = 'animated-background';
    this.canvas.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: -1;
      opacity: 0.8;
    `;
    
    document.body.appendChild(this.canvas);
    this.ctx = this.canvas.getContext('2d');
    this.resizeCanvas();
  }

  resizeCanvas() {
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
  }

  createParticles() {
    const particleCount = 60;
    const colors = ['#7c3aed', '#4f46e5', '#ec4899', '#10b981', '#f59e0b'];
    
    for (let i = 0; i < particleCount; i++) {
      this.particles.push({
        x: Math.random() * this.canvas.width,
        y: Math.random() * this.canvas.height,
        size: Math.random() * 3 + 1,
        speedX: (Math.random() - 0.5) * 1,
        speedY: (Math.random() - 0.5) * 1,
        color: colors[Math.floor(Math.random() * colors.length)],
        opacity: Math.random() * 0.6 + 0.2,
        pulsePhase: Math.random() * Math.PI * 2,
        pulseSpeed: Math.random() * 0.02 + 0.01
      });
    }
  }

  setupEventListeners() {
    window.addEventListener('resize', () => this.resizeCanvas());
    
    window.addEventListener('mousemove', (e) => {
      this.mouse.x = e.clientX;
      this.mouse.y = e.clientY;
    });
  }

  updateParticles() {
    this.particles.forEach(particle => {
      particle.x += particle.speedX;
      particle.y += particle.speedY;
      
      if (particle.x < 0 || particle.x > this.canvas.width) {
        particle.speedX *= -1;
      }
      if (particle.y < 0 || particle.y > this.canvas.height) {
        particle.speedY *= -1;
      }
      
      const dx = this.mouse.x - particle.x;
      const dy = this.mouse.y - particle.y;
      const distance = Math.sqrt(dx * dx + dy * dy);
      
      if (distance < 100) {
        const force = (100 - distance) / 100;
        particle.x -= (dx / distance) * force * 2;
        particle.y -= (dy / distance) * force * 2;
      }
      
      particle.pulsePhase += particle.pulseSpeed;
    });
  }

  drawParticles() {
    this.particles.forEach(particle => {
      const pulse = Math.sin(particle.pulsePhase) * 0.3 + 1;
      const size = particle.size * pulse;
      
      const gradient = this.ctx.createRadialGradient(
        particle.x, particle.y, 0,
        particle.x, particle.y, size * 3
      );
      gradient.addColorStop(0, particle.color + '40');
      gradient.addColorStop(1, particle.color + '00');
      
      this.ctx.fillStyle = gradient;
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, size * 3, 0, Math.PI * 2);
      this.ctx.fill();
      
      this.ctx.fillStyle = particle.color + Math.floor(particle.opacity * 255).toString(16).padStart(2, '0');
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, size, 0, Math.PI * 2);
      this.ctx.fill();
    });
  }

  drawConnections() {
    const maxDistance = 120;
    
    for (let i = 0; i < this.particles.length; i++) {
      for (let j = i + 1; j < this.particles.length; j++) {
        const p1 = this.particles[i];
        const p2 = this.particles[j];
        const dx = p1.x - p2.x;
        const dy = p1.y - p2.y;
        const distance = Math.sqrt(dx * dx + dy * dy);
        
        if (distance < maxDistance) {
          const opacity = (1 - distance / maxDistance) * 0.3;
          
          const gradient = this.ctx.createLinearGradient(p1.x, p1.y, p2.x, p2.y);
          gradient.addColorStop(0, p1.color + Math.floor(opacity * 255).toString(16).padStart(2, '0'));
          gradient.addColorStop(1, p2.color + Math.floor(opacity * 255).toString(16).padStart(2, '0'));
          
          this.ctx.strokeStyle = gradient;
          this.ctx.lineWidth = 1;
          this.ctx.beginPath();
          this.ctx.moveTo(p1.x, p1.y);
          this.ctx.lineTo(p2.x, p2.y);
          this.ctx.stroke();
        }
      }
    }
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    
    const bgGradient = this.ctx.createLinearGradient(0, 0, this.canvas.width, this.canvas.height);
    bgGradient.addColorStop(0, 'rgba(124, 58, 237, 0.02)');
    bgGradient.addColorStop(0.5, 'rgba(79, 70, 229, 0.02)');
    bgGradient.addColorStop(1, 'rgba(236, 72, 153, 0.02)');
    
    this.ctx.fillStyle = bgGradient;
    this.ctx.fillRect(0, 0, this.canvas.width, this.canvas.height);
    
    this.updateParticles();
    this.drawConnections();
    this.drawParticles();
    
    requestAnimationFrame(() => this.animate());
  }
}

// Confetti Celebration
class Confetti {
  constructor() {
    this.particles = [];
    this.canvas = null;
    this.ctx = null;
  }

  create() {
    this.canvas = document.createElement('canvas');
    this.canvas.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      pointer-events: none;
      z-index: 9999;
    `;
    
    document.body.appendChild(this.canvas);
    this.ctx = this.canvas.getContext('2d');
    this.canvas.width = window.innerWidth;
    this.canvas.height = window.innerHeight;
    
    this.createParticles();
    this.animate();
    
    setTimeout(() => this.cleanup(), 3000);
  }

  createParticles() {
    const colors = ['#7c3aed', '#4f46e5', '#ec4899', '#10b981', '#f59e0b'];
    const centerX = this.canvas.width / 2;
    const centerY = this.canvas.height / 3;
    
    for (let i = 0; i < 100; i++) {
      const angle = (Math.PI * 2 * i) / 100;
      const velocity = 30 + Math.random() * 10;
      
      this.particles.push({
        x: centerX,
        y: centerY,
        vx: Math.cos(angle) * velocity,
        vy: Math.sin(angle) * velocity,
        color: colors[Math.floor(Math.random() * colors.length)],
        size: Math.random() * 6 + 2,
        life: 150,
        opacity: 1
      });
    }
  }

  updateParticles() {
    this.particles.forEach(particle => {
      particle.x += particle.vx;
      particle.y += particle.vy;
      particle.vy += 0.3;
      particle.vx *= 0.98;
      particle.vy *= 0.98;
      particle.life--;
      particle.opacity = particle.life / 150;
      
      if (particle.y > this.canvas.height - particle.size) {
        particle.y = this.canvas.height - particle.size;
        particle.vy *= -0.8;
      }
    });
    
    this.particles = this.particles.filter(particle => particle.life > 0);
  }

  drawParticles() {
    this.particles.forEach(particle => {
      this.ctx.save();
      this.ctx.globalAlpha = particle.opacity;
      this.ctx.fillStyle = particle.color;
      this.ctx.beginPath();
      this.ctx.arc(particle.x, particle.y, particle.size, 0, Math.PI * 2);
      this.ctx.fill();
      this.ctx.restore();
    });
  }

  animate() {
    this.ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);
    
    this.updateParticles();
    this.drawParticles();
    
    if (this.particles.length > 0) {
      requestAnimationFrame(() => this.animate());
    } else {
      this.cleanup();
    }
  }

  cleanup() {
    if (this.canvas && this.canvas.parentNode) {
      this.canvas.parentNode.removeChild(this.canvas);
    }
  }
}

// Initialize components
document.addEventListener('DOMContentLoaded', () => {
  new AnimatedBackground();
  
  // Make confetti globally available
  window.triggerConfetti = () => {
    new Confetti().create();
  };
});

// Add some extra interactive features
document.addEventListener('DOMContentLoaded', () => {
  // Smooth scroll for navigation links
  document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener('click', function (e) {
      e.preventDefault();
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        target.scrollIntoView({ behavior: 'smooth' });
      }
    });
  });
  
  // Add hover effects to cards
  document.querySelectorAll('.group').forEach(card => {
    card.addEventListener('mouseenter', () => {
      card.style.transform = 'translateY(-8px)';
    });
    card.addEventListener('mouseleave', () => {
      card.style.transform = 'translateY(0)';
    });
  });
  
  // Add loading animation to form
  const form = document.querySelector('form');
  if (form) {
    form.addEventListener('submit', () => {
      const button = form.querySelector('button[type="submit"]');
      if (button) {
        button.disabled = true;
        button.innerHTML = `
          <div class="flex items-center justify-center">
            <div class="animate-spin rounded-full h-5 w-5 border-b-2 border-white mr-3"></div>
            Processing...
          </div>
        `;
      }
    });
  }
});
