import React, { useEffect, useRef } from 'react';

const StarsBackground = () => {
    const canvasRef = useRef(null);
    const requestRef = useRef();
    
    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');
        const width = canvas.width = window.innerWidth;
        const height = canvas.height = window.innerHeight;

        const resizeCanvas = () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        };
        window.addEventListener('resize', resizeCanvas);
        resizeCanvas();

        
        let stars = Array(400).fill().map(() => createStar(width, height));
        let shootingStars = []; // Array to hold shooting stars

        function createStar(width, height) {
            return {
                x: Math.random() * width,
                y: Math.random() * height,
                opacity: Math.random(),
                speed: 0.01 + Math.random() * 0.01, // Adjusted for a gentle fade
            };
        }

        function createShootingStar() {
            const angle = Math.random() * 2 * Math.PI; // Any direction
            return {
                x: Math.random() * width,
                y: Math.random() * height,
                length: Math.random() * 20 + 10,
                opacity: 1,
                angle: angle,
                speed: Math.random() * 5 + 10, // Adjusted for visible movement
            };
        }

        function updateStars() {
            stars.forEach(star => {
                star.opacity += star.speed * (Math.random() > 0.5 ? 1 : -1); // Randomly increase or decrease opacity
                if (star.opacity <= 0) {
                    star.opacity = 0;
                    star.speed = Math.abs(star.speed); // Ensure the speed is positive for fade in
                } else if (star.opacity >= 1) {
                    star.opacity = 1;
                    star.speed = -Math.abs(star.speed); // Ensure the speed is negative for fade out
                }
            });
        }

        function updateShootingStars() {
            shootingStars = shootingStars.filter(star => star.opacity > 0);
            shootingStars.forEach(star => {
                star.x += Math.cos(star.angle) * star.speed;
                star.y += Math.sin(star.angle) * star.speed;
                star.opacity -= 0.05; // Gradually fade out
            });

            if (Math.random() < 0.005) { 
                shootingStars.push(createShootingStar());
            }
        }

        function draw() {
            ctx.clearRect(0, 0, width, height);

            // Draw twinkling stars
            stars.forEach(star => {
                ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity})`;
                ctx.beginPath();
                ctx.arc(star.x, star.y, 1, 0, Math.PI * 2);
                ctx.fill();
            });

            // Draw shooting stars
            shootingStars.forEach(star => {
                ctx.beginPath();
                ctx.moveTo(star.x, star.y);
                ctx.lineTo(star.x - Math.cos(star.angle) * star.length, 
                           star.y - Math.sin(star.angle) * star.length);
                ctx.strokeStyle = `rgba(255, 255, 255, ${star.opacity})`;
                ctx.lineWidth = 2;
                ctx.stroke();
            });

            updateStars();
            updateShootingStars();

            requestRef.current = requestAnimationFrame(draw); 
        }

        draw();
        
        return () => {
            cancelAnimationFrame(requestRef.current);
            window.removeEventListener('resize', resizeCanvas);
        };
        
    }, []);

    return(
        <canvas ref={canvasRef} style={{ position: 'absolute', top: 0, left: 0, zIndex: 6, width: '100%', height: '100%', pointerEvents: 'none'}} />
    );
};

export default StarsBackground;
