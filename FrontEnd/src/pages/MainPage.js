import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from '../css/main.module.css';
import { tailspin } from 'ldrs'

tailspin.register()

const MainPage = () => {
    const [topic, setTopic] = useState('');
    const [showButton, setShowButton] = useState(false);
    const navigate = useNavigate();
    const [trendingTopics, setTrendingTopics] = useState([]);
    const [isLoading, setIsLoading] = useState(false);

    useEffect(() => {
        const fetchTrendingTopics = async () => {
            try {
                const response = await fetch('http://127.0.0.1:7000/trending');
                const topics = await response.json();
                setTrendingTopics(topics);
            } catch (error) {
                console.error('Failed to fetch trending topics:', error);
            }
        };
    
        fetchTrendingTopics();
    }, []);

    useEffect(() => {
        if (topic) {
            setShowButton(true);
        } else {
            setShowButton(false);
        }
    }, [topic]); 

    const handleSubmit = async (e) => {
        e.preventDefault();
        setIsLoading(true);
    
        if (!topic) {
            console.log('Topic is required');
            return;
        }
    
        try {
            const response = await fetch('http://127.0.0.1:7000/videos_preview', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ video: topic }),
            });
    
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
    
            const data = await response.json();
            navigate('/preview', { state: { videosInfo: data } });
            setIsLoading(false);
        } catch (error) {
            console.error('Error during submission:', error);
        }
    };
    
        
    return (
        <div className={styles.mainContainer}>
            <div className={styles.splitContainer}>
            <div className={styles.leftContainer}>
                <h1 className={styles.gradientText} style={{fontFamily: 'Yeseva One'}}>VidJalsa</h1>
                <h1 className={styles.gradientText} style={{fontSize: '3rem'}} >Informative Storytelling, <br/>Made Easy</h1>

            </div>
            
            <div className={styles.rightContainer} >
                <div className={styles.inputContainer}>
                    <label htmlFor="topicInput" className={styles.inputLabel}>Choose A Topic To Create A Blog For,<br/> Try To Be Specific</label>
                    <form onSubmit={handleSubmit} className={styles.formContainer}>
                        <input
                            id="topicInput"
                            type="text"
                            className={topic ? 'withButton' : ''}
                            value={topic}
                            onChange={(e) => setTopic(e.target.value)}
                            onKeyDown={(e) => e.key === 'Enter' && handleSubmit(e)} 
                        />
                        {topic && (
                            <>
                                <button 
                                    type="submit" 
                                    className={`${styles.submitArrowButton} ${showButton ? styles.buttonShow : styles.buttonHide}`}
                                    aria-label="Submit"
                                    disabled={isLoading} // Disable button when loading
                                >
                                    <svg viewBox="0 0 24 24" width="24" height="24" stroke="currentColor" strokeWidth="2" fill="none" strokeLinecap="round" strokeLinejoin="round" className="feather feather-arrow-right">
                                        <line x1="5" y1="12" x2="19" y2="12"></line>
                                        <polyline points="12 5 19 12 12 19"></polyline>
                                    </svg>
                                </button>
                                {isLoading && (
                                    <l-tailspin
                                        size="30"
                                        stroke="5"
                                        speed="0.9" 
                                        color="white"
                                        style={{marginBottom: '0.9rem'}}
                                    ></l-tailspin>
                                )}
                            </>
                        )}
                    </form>
                    <div className={styles.divider} >
                        <span className={styles.line} ></span>
                        <span className={styles.dividerText} >Or Pick A Trendy Topic</span>
                        <span className={styles.line} ></span>
                    </div>
                    <div className={styles.trendingTopicsContainer} >
                        {trendingTopics.map((topic, index) => (
                            <button
                                key={index}
                                className={styles.topicBubble} 
                                onClick={() => setTopic(topic)} 
                            >
                                {topic}
                            </button>
                        ))}
                    </div>
                </div>
            </div>
        </div>
        </div>
    );
};

export default MainPage;
