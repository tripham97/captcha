'use client'
import { useEffect, useState } from 'react';

type ImageItem = {
  id: string;
  filename: string;
};

export default function Home() {
  const [label, setLabel] = useState('');
  const [images, setImages] = useState<ImageItem[]>([]);
  const [selected, setSelected] = useState<string[]>([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    // Fetch challenge from your Flask backend
    fetch('http://localhost:5000/api/captcha')  // adjust if needed
      .then(res => res.json())
      .then(data => {
        setLabel(data.label);
        setImages(data.images);
      });
  }, []);

  const loadImage = () => {
    setTimeout(() => setLoading(true), 10000000);
    fetch("http://localhost:5000/api/captcha")
      .then((res) => res.json())
      .then((data) => {
        setLabel(data.label);
        setImages(data.images);
        setSelected([]);
        // setTimeout(() => setLoading(true), 3000);
      })
      .finally(() => setLoading(false)); 
      
  };
  

  const toggleSelect = (id: string) => {
    setSelected(prev =>
      prev.includes(id) ? prev.filter(i => i !== id) : [...prev, id]
    );
  };

  const loadCaptcha = () => {
    fetch("http://localhost:5000/api/captcha")
      .then((res) => res.json())
      .then((data) => {
        setLabel(data.label);
        setImages(data.images);
        setSelected([]);
      });
  };
  
  useEffect(() => {
    loadCaptcha();
  }, []);

  const handleSubmit = async () => {
    const response = await fetch("http://localhost:5000/api/check", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        selected,
        label,
        images: images.map((img) => img.id),
      }),
    });
  
    const text = await response.text(); 
    alert(text); 
    
  if (text === "Missing or Wrong images ❌") {
    setSelected([]);
    loadCaptcha(); 
  }
  if (text === "You passed ✅ the CAPTCHA!") {
    setSelected([]);
    loadCaptcha(); 
  }
  };

  return (
    <div className="grid grid-rows-[20px_1fr_20px] items-center justify-items-center min-h-screen p-8 pb-2 gap-2  font-[family-name:var(--font-geist-sans)] text-foreground">
      <main className="flex flex-col gap-[32px] row-start-2 items-center sm:items-start">
      <h2 className="text-2xl font-bold text-center sm:text-left">reCAPTCHA Challenge</h2>
        <ul className="list-inside list-decimal text-sm/6 text-center sm:text-left font-[family-name:var(--font-geist-mono)]">
          <li className="mb-2 tracking-[-.01em]">
            Select all images with a <strong>{label}</strong>.
          </li>
        </ul>


        <div className="p-6">
      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="w-6 h-6 rounded-full bg-black shadow-[0_0_0_0_rgba(0,0,0,0.25)] animate-ping" />
        </div>
      ) : (
          <div style={{ display: 'flex', flexWrap: 'wrap' }}>
        
            {images.map(img => (
              <img
                key={img.id}
                src={`http://localhost:5000/static/images/${img.id}.png`}  // adjust if needed
                alt={img.id}
                // onLoad={loadImage}
                onClick={() => toggleSelect(img.id)}
                style={{
                  width: 150,
                  borderRadius: 5,
                  objectFit: 'cover',
                  margin: 5,            
                  border: selected.includes(img.id) ? '3px solid limegreen' : '3px solid gray',
                  cursor: 'pointer',
                }}
              />
            ))}
          </div>
      )}
      </div>

      <a className="rounded-full border border-solid border-transparent transition-colors flex items-center justify-center bg-foreground text-background gap-2 hover:bg-[#383838] dark:hover:bg-[#ccc] font-medium text-sm sm:text-base h-10 sm:h-12 px-4 sm:px-5 sm:w-auto" onClick={handleSubmit} style={{ marginTop: 20 }}>Submit</a>
      </main>
    </div>
  );
}
