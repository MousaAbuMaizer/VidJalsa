import React, { useEffect, useRef, useState, useMemo } from 'react';
import { useLocation } from 'react-router-dom';
import styles from '../css/output.module.css';

function OutputPage() {
    const containerRef = useRef(null);
    const [centerIndex, setCenterIndex] = useState(null);
    const [isFirstItemCentered, setIsFirstItemCentered] = useState(true);
    const [isLastItemCentered, setIsLastItemCentered] = useState(false);
    const { state } = useLocation();
    const videosInfo = useMemo(() => state?.videosInfo || [], [state.videosInfo]);
    const deploymentUrl = state?.deploymentUrl;

    const scrollToNext = () => {
        const container = containerRef.current;
        if (!container || centerIndex === null || videosInfo.length === 0) return;

        let nextIndex = centerIndex + 1;
        if (nextIndex >= videosInfo.length) return;

        const nextItem = container.children[nextIndex];
        if (nextItem) {
            const topPos = nextItem.offsetTop - (container.offsetHeight / 2) + (nextItem.offsetHeight / 2);
            container.scrollTo({ top: topPos, behavior: 'smooth' });
        }
    };


    const scrollToPrev = () => {
        const container = containerRef.current;
        if (!container || centerIndex === null || videosInfo.length === 0) return;

        if (centerIndex === 0) {
            container.scrollTo({ top: 0, behavior: 'smooth' });
            return;
        }

        let targetIndex = centerIndex - 1;
        targetIndex = Math.max(targetIndex, 0);

        const targetItem = container.children[targetIndex];
        if (targetItem) {
            const topPos = targetItem.offsetTop - (container.offsetHeight / 2) + (targetItem.offsetHeight / 2);
            container.scrollTo({ top: topPos, behavior: 'smooth' });
        }
    };

    useEffect(() => {
        const calculateCenterIndex = () => {
            const container = containerRef.current;
            const scrollTop = container.scrollTop;
            const containerHeight = container.offsetHeight;
            let closestIndex = null;
            let closestDistance = null;
            const children = container.children; 

            for (let i = 0; i < children.length; i++) {
                const child = children[i];
                const childTop = child.offsetTop - container.offsetTop;
                const childHeight = child.offsetHeight;
                const childCenter = childTop + childHeight / 2;
                const containerCenter = scrollTop + containerHeight / 2;
                const distance = Math.abs(containerCenter - childCenter);

                if (closestDistance === null || distance < closestDistance) {
                    closestDistance = distance;
                    closestIndex = i;
                }
            }
            setCenterIndex(closestIndex);

            setIsFirstItemCentered(closestIndex === 0);
            setIsLastItemCentered(closestIndex === videosInfo.length - 1);
        };

        const container = containerRef.current;
        container.addEventListener('scroll', calculateCenterIndex);
        calculateCenterIndex(); 

        return () => container.removeEventListener('scroll', calculateCenterIndex);
    }, [videosInfo]);

    const handlePeekClick = () => {
        window.open(deploymentUrl, '_blank');
    };

  
    return (
    <div className={styles.mainContainer}>
        <div className={styles.leftContainer}>
            <h1 className={styles.gradientText} style={{fontFamily: 'Yeseva One', marginBottom:'30px'}}>Your Website Is Ready</h1>            
                <button className={`${styles.button} ${styles.peekButton}`} onClick={handlePeekClick}>
                    Take A Look 👀
                </button>
            </div>

            <div className={styles.fadeContainer}> 
                {<button className={`${styles.scrollButton} ${!isFirstItemCentered ? styles.visible : ''}`} onClick={scrollToPrev}>&#9650;</button>}
                <div className={styles.topFade}></div> 
                <div className={styles.rightContainer} ref={containerRef}>
                {videosInfo && videosInfo.map((video, index) => (
                    <div key={index} className={`${styles.videoContainer} ${index === centerIndex ? styles.centered : ''}`}>
                        <div className={styles.videoContent}>
                            <div className={styles.videoThumbnailContainer}>
                                <a href={video.link} target="_blank" rel="noopener noreferrer" className={styles.videoLink}>
                                    <img src={video.thumbnail} alt={video.title} className={styles.videoThumbnail} />
                                </a>
                            </div>
                        </div>
                        <p className={`${styles.videoTitle} ${index === centerIndex ? styles.visible : ''}`}>{video.title}</p>
                    </div>
                ))}
                </div>
                <div className={styles.bottomFade}></div> 
                {<button className={`${styles.scrollButton} ${!isLastItemCentered ? styles.visible : ''}`} onClick={scrollToNext}>&#9660;</button>}
            </div>
    </div>
    
    );
}

export default OutputPage;