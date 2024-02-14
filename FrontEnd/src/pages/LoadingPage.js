import React from 'react';
import styles from '../css/loading.module.css';
import MeteorShowers from '../components/MeteorShowers';

function LoadingPage() {
    return (
        <div className={styles.mainContainer}>
            <MeteorShowers />
            <div className={styles.loadingContainer}>
                <h1 className={styles.gradientText} style={{fontFamily: 'Yeseva One'}}>Creating Your Blog</h1>
                <h1 className={styles.gradientText} style={{fontSize: '3rem', marginBottom: '20px'}}>This Might Take A While...</h1>
            </div>
        </div>
    );
}

export default LoadingPage;
