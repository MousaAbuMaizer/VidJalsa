import React, { useEffect, useRef } from 'react';
import styles from '../css/meteors.module.css';

function MeteorShowers() {
    const canvasRef = useRef(null);

    useEffect(() => {
        const canvas = canvasRef.current;
        const ctx = canvas.getContext('2d');

        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;

        const meteors = [];

        function createMeteor() {
            const x = Math.random() * canvas.width;
            const y = 0;
            const length = Math.random() * (80 - 30) + 30; // Meteor length between 30 and 80
            const speed = Math.random() * (10 - 5) + 5; // Speed between 5 and 10

            meteors.push({ x, y, length, speed });
        }

        function drawMeteors() {
            ctx.clearRect(0, 0, canvas.width, canvas.height);
            meteors.forEach((meteor, index) => {
                ctx.beginPath();
                ctx.moveTo(meteor.x, meteor.y);
                ctx.lineTo(meteor.x + meteor.length, meteor.y + meteor.length);
                ctx.strokeStyle = 'white';
                ctx.lineWidth = 0.8;
                ctx.stroke();

                // Update meteor position
                meteor.x += meteor.speed;
                meteor.y += meteor.speed;

                // Remove meteors that move off screen
                if (meteor.x > canvas.width || meteor.y > canvas.height) {
                    meteors.splice(index, 1);
                }
            });

            // Randomly add new meteors
            if (Math.random() < 0.1) {
                createMeteor();
            }

            requestAnimationFrame(drawMeteors);
        }

        drawMeteors();

        // Handle window resizing
        function resize() {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        }
        window.addEventListener('resize', resize);

        return () => {
            window.removeEventListener('resize', resize);
        };
    }, []);

    return (
        <canvas ref={canvasRef} className={styles.canvas}></canvas>
    );
}

export default MeteorShowers;