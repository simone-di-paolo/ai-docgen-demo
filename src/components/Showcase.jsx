import React from 'react';
import '../App.css';

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

function Showcase() {
  const items = [
    {
      image: 'https://images.unsplash.com/photo-1605379399642-870262d3d051?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTc5fDB8MXxzZWFyY2h8N3x8ZGV2ZWxvcGVyfGVufDB8fHx8MTY3MTAxODQwMg&ixlib=rb-4.0.3&q=80&w=1080',
      title: 'Dashboard Moderna',
      tags: ['React', 'Charts', 'Admin'],
    },
    {
      image: 'https://images.unsplash.com/photo-1542744173-8e7e53415bb0?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTc5fDB8MXxzZWFyY2h8MTB8fHdlYiUyMGRlc2lnbnxlbnwwfHx8fDE2NzEwMTg0NDM&ixlib=rb-4.0.3&q=80&w=1080',
      title: 'Landing Page d\'Impatto',
      tags: ['UI/UX', 'Marketing', 'Web'],
    },
    {
      image: 'https://images.unsplash.com/photo-1555949963-ff9fe0c870eb?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTc5fDB8MXxzZWFyY2h8MTV8fHByb2dyYW1taW5nfGVufDB8fHx8MTY3MTAxODQ4MQ&ixlib=rb-4.0.3&q=80&w=1080',
      title: 'Piattaforma E-commerce',
      tags: ['Shopping', 'React', 'API'],
    },
     {
      image: 'https://images.unsplash.com/photo-1517694712202-1428bc648cfo?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNTc5fDB8MXxzZWFyY2h8MTV8fHByb2dyYW1taW5nfGVufDB8fHx8MTY3MTAxODQ4MQ&ixlib=rb-4.0.3&q=80&w=1080',
      title: 'App Mobile Ibrida',
      tags: ['React Native', 'Mobile', 'UX'],
    }
  ];

  return (
    <section className="showcase">
      <h2 className="section-title">Vetrina dei Progetti</h2>
      <div className="showcase-grid">
        {items.map((item, index) => <ShowcaseItem key={index} {...item} />)}
      </div>
    </section>
  );
}

export default Showcase;
