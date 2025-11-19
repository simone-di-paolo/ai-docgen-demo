import React, { useState } from 'react';
import './Showcase.css';

const ShowcaseItem = ({ image, title, tags }) => (
  <div className="showcase-item">
    <img src={image} alt={title} className="showcase-image" />
    <div className="showcase-overlay">
      <h4 className="showcase-title">{title}</h4>
      <div className="showcase-tags">
        {tags.map(tag => <span key={tag} className="tag">{tag}</span>)}
      </div>
    </div>
  </div>
);

const initialItems = [
    {
      image: 'https://images.unsplash.com/photo-1605379399642-870262d3d051?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTc5fDB8MXxzZWFyY2h8N3x8ZGV2ZWxvcGVyfGVufDB8fHx8MTY3MTAxODQwMg&ixlib=rb-4.0.3&q=80&w=1080',
      title: 'Modern Dashboard',
      tags: ['React', 'Charts', 'Admin'],
    },
    {
      image: 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTc5fDB8MXxzZWFyY2h8MTB8fHdlYiUyMGRlc2lnbnxlbnwwfHx8fDE2NzEwMTg0NDM&ixlib=rb-4.0.3&q=80&w=1080',
      title: 'Impactful Landing Page',
      tags: ['UI/UX', 'Marketing', 'Web'],
    },
    {
      image: 'https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTc5fDB8MXxzZWFyY2h8MTV8fHByb2dyYW1taW5nfGVufDB8fHx8MTY3MTAxODQ4MQ&ixlib=rb-4.0.3&q=80&w=1080',
      title: 'E-commerce Platform',
      tags: ['Shopping', 'React', 'API'],
    },
     {
      image: 'https://images.unsplash.com/photo-1517694712202-1428bc648cfo?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTc5fDB8MXxzZWFyY2h8MTV8fHByb2dyYW1taW5nfGVufDB8fHx8MTY3MTAxODQ4MQ&ixlib=rb-4.0.3&q=80&w=1080',
      title: 'Hybrid Mobile App',
      tags: ['React Native', 'Mobile', 'UX'],
    }
  ];

const newItems = [
  {
    image: 'https://images.unsplash.com/photo-1587620962725-abab7fe55159?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1080&q=80',
    title: 'SaaS Platform',
    tags: ['Cloud', 'Web App', 'API'],
  },
  {
    image: 'https://images.unsplash.com/photo-1516116216624-53e697314e7e?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1080&q=80',
    title: 'Cybersecurity Dashboard',
    tags: ['Security', 'Analytics', 'Admin'],
  },
];

function Showcase() {
  const [items, setItems] = useState(initialItems);
  const [isLoading, setIsLoading] = useState(false);
  const [hasLoaded, setHasLoaded] = useState(false);

  const handleLoadMore = () => {
    setIsLoading(true);
    setTimeout(() => {
      setItems(prevItems => [...prevItems, ...newItems]);
      setIsLoading(false);
      setHasLoaded(true);
    }, 1500); // Simulate network delay
  };

  return (
    <section className="showcase">
      <h2 className="section-title">Project Showcase</h2>
      <div className="showcase-grid">
        {items.map((item, index) => <ShowcaseItem key={index} {...item} />)}
      </div>
      <div className="showcase-actions">
        {!hasLoaded && (
          <button onClick={handleLoadMore} disabled={isLoading} className="load-more-button">
            {isLoading ? <div className="loader"></div> : 'Load More'}
          </button>
        )}
      </div>
    </section>
  );
}

export default Showcase;
