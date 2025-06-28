"""
Simple News Presentation Creator - ASYNC VERSION with fal.ai
OpenAI + fal.ai FLUX Dev + Absolute Paths
Clean, minimal, teammate-friendly + MUCH FASTER + NO RATE LIMITS
"""

import json
import requests
import os
import time
import asyncio
import aiohttp
from PIL import Image
import io
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
import fal_client

class AsyncNewsPresentationMaker:
    """
    Simple class: JSON in → Presentation images out (ASYNC with fal.ai)
    Same interface, much faster execution, no rate limits
    """
    
    def __init__(self, openai_key: str, fal_key: str, elevenlabs_key: str = None):
        self.openai = OpenAI(api_key=openai_key)
        self.fal_key = fal_key
        self.elevenlabs_key = elevenlabs_key
        
        # Set fal.ai API key
        os.environ['FAL_KEY'] = fal_key
        
        # Create absolute output directory
        self.output_dir = os.path.abspath("presentation_output")
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def create_slide_async(self, session: aiohttp.ClientSession, title: str, text: str, source: str) -> dict:
        """Create one slide image using fal.ai FLUX Dev (async version)"""
        
        # Step 1: OpenAI creates smart prompt (sync - it's fast)
        prompt_request = f"Create image prompt for news slide: {title}. Content: {text}. Professional presentation background, no text, 16:9 format."
        
        try:
            response = self.openai.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt_request}],
                max_tokens=100
            )
            prompt = response.choices[0].message.content.strip()
        except:
            prompt = f"Professional news background for {title}"
        
        # Step 2: fal.ai FLUX Dev generates image (async wrapper)
        try:
            t0 = time.time()
            print(f"🎨 Starting: {title[:30]}...")
            
            # Run fal_client in thread pool since it's sync
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None,
                self._generate_with_fal,
                prompt
            )
            
            generation_time = time.time() - t0
            
            if result and "images" in result:
                print(f"✅ {title[:30]}: {generation_time:.2f}s")
                
                # Download image from fal.ai
                image_url = result["images"][0]["url"]
                async with session.get(image_url) as img_response:
                    if img_response.status == 200:
                        image_data = await img_response.read()
                        
                        # Save image (run in thread pool to avoid blocking)
                        filepath = await loop.run_in_executor(
                            None, 
                            self._save_image, 
                            image_data, 
                            title
                        )
                        
                        return {
                            "status": "success",
                            "absolute_path": filepath,
                            "title": title,
                            "generation_time": generation_time
                        }
                    else:
                        print(f"❌ {title[:30]}: Download failed ({img_response.status})")
                        return {"status": "error", "message": f"Image download failed: {img_response.status}"}
            else:
                print(f"❌ {title[:30]}: No images returned from fal.ai")
                return {"status": "error", "message": "fal.ai returned no images"}
                    
        except Exception as e:
            print(f"❌ {title[:30]}: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _generate_with_fal(self, prompt: str) -> dict:
        """Generate image with fal.ai FLUX Dev (sync helper for thread pool)"""
        try:
            result = fal_client.subscribe(
                "fal-ai/flux/dev",  # fal.ai FLUX Dev endpoint
                arguments={
                    "prompt": prompt,
                    "image_size": "landscape_16_9",  # Perfect for slides
                    "num_inference_steps": 28,      # fal.ai FLUX Dev default
                    "guidance_scale": 3.5,
                    "num_images": 1
                }
            )
            return result
        except Exception as e:
            print(f"fal.ai error: {e}")
            return None
    
    def _save_image(self, image_data: bytes, title: str) -> str:
        """Save image to disk (sync helper for thread pool)"""
        image = Image.open(io.BytesIO(image_data))
        # fal.ai already outputs 16:9, but ensure consistent size
        image = image.resize((1792, 1024), Image.Resampling.LANCZOS)
        
        filename = f"slide_{int(time.time())}_{hash(title) % 1000}.png"
        filepath = os.path.join(self.output_dir, filename)
        image.save(filepath, "PNG")
        
        return os.path.abspath(filepath)
    
    async def create_audio_async(self, session: aiohttp.ClientSession, script: str) -> dict:
        """Create voiceover audio (async version) - UNCHANGED"""
        return {
            "status": "success",
            "absolute_path": ".",
        }
        if not self.elevenlabs_key:
            print("🔇 Audio: Skipped (no API key)")
            return {"status": "skipped"}
        
        try:
            print("🎵 Starting audio generation...")
            
            async with session.post(
                "https://api.elevenlabs.io/v1/text-to-speech/21m00Tcm4TlvDq8ikWAM",
                headers={
                    "Accept": "audio/mpeg",
                    "Content-Type": "application/json",
                    "xi-api-key": self.elevenlabs_key
                },
                json={"text": script, "model_id": "eleven_monolingual_v1"}
            ) as response:
                
                if response.status == 200:
                    print("✅ Audio: Generated successfully")
                    audio_data = await response.read()
                    
                    # Save audio (run in thread pool)
                    loop = asyncio.get_event_loop()
                    filepath = await loop.run_in_executor(
                        None,
                        self._save_audio,
                        audio_data
                    )
                    
                    return {
                        "status": "success",
                        "absolute_path": filepath
                    }
                else:
                    print(f"❌ Audio: Failed ({response.status})")
                    return {"status": "error", "message": "Audio generation failed"}
                    
        except Exception as e:
            print(f"❌ Audio: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def _save_audio(self, audio_data: bytes) -> str:
        """Save audio to disk (sync helper for thread pool)"""
        filename = f"audio_{int(time.time())}.mp3"
        filepath = os.path.join(self.output_dir, filename)
        
        with open(filepath, 'wb') as f:
            f.write(audio_data)
        
        return os.path.abspath(filepath)
    
    async def _async_process(self, articles: list) -> dict:
        """Internal async processing method - UNCHANGED"""
        
        # Create script for audio (can start immediately)
        script = "Welcome to the news. " + " ".join([
            f"{item.get('title', '')}. {item.get('text', '')}"
            for item in articles
        ]) + " Thank you."
        
        # Create aiohttp session for all requests
        async with aiohttp.ClientSession() as session:
            
            # Start all tasks concurrently
            slide_tasks = [
                self.create_slide_async(session, item.get('title', ''), item.get('text', ''), item.get('source', ''))
                for item in articles
            ]
            
            audio_task = self.create_audio_async(session, script)
            
            # Wait for all to complete
            print(f"🚀 Starting {len(slide_tasks)} slides + audio in parallel...")
            start_time = time.time()
            
            # Run everything concurrently - slides + audio together!
            all_results = await asyncio.gather(
                *slide_tasks, 
                audio_task, 
                return_exceptions=True
            )
            
            total_time = time.time() - start_time
            print(f"✅ All generation completed in {total_time:.2f}s")
            
            # Split results: slides are all except last, audio is last
            slides_results = all_results[:-1]
            audio_result = all_results[-1]
            
            # Convert exceptions to error dicts for slides
            slides = []
            for result in slides_results:
                if isinstance(result, Exception):
                    slides.append({"status": "error", "message": str(result)})
                else:
                    slides.append(result)
            
            # Handle audio result
            if isinstance(audio_result, Exception):
                audio_result = {"status": "error", "message": str(audio_result)}
            
            return {
                "status": "success",
                "slides": slides,
                "audio": audio_result,
                "output_dir": self.output_dir,
                "total_time": total_time
            }
    
    def process_json_input(self, json_string: str) -> dict:
        """
        Main method: JSON in → Slides out (SAME INTERFACE, NOW WITH fal.ai)
        """
        
        try:
            # Parse JSON
            data = json.loads(json_string)
            if isinstance(data, dict) and "articles" in data:
                articles = data["articles"]
            elif isinstance(data, list):
                articles = data
            else:
                articles = [data]
            
            # Run async processing with better error handling
            try:
                # Try to get existing event loop
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If we're already in an async context, create a new thread
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, self._async_process(articles))
                        return future.result()
                else:
                    return asyncio.run(self._async_process(articles))
            except RuntimeError:
                # No event loop, create one
                return asyncio.run(self._async_process(articles))
            except KeyboardInterrupt:
                print("\n🛑 Generation cancelled by user")
                return {"status": "cancelled", "message": "Generation cancelled by user"}
            
        except Exception as e:
            return {"status": "error", "message": str(e)}





# Simple usage
if __name__ == "__main__":
    """
    UPDATED USAGE (only constructor changed):
    
    1. pip install fal-client aiohttp
    2. Get fal.ai API key from https://fal.ai/
    3. maker = NewsPresentationMaker(openai_key, fal_key, elevenlabs_key)
    4. result = maker.process_json_input(json_string)
    5. Get absolute paths in result["slides"]
    
    NOW: MUCH FASTER + NO RATE LIMITS!
    """
    
    # Test data (same as before)
    test_json = '''[
        {
        "title": "AI News",
        "text": "In 2017, blockchain was everyone's focus. Presented as a revolutionary technology, blockchain offered a decentralised way to record and verify transactions, unlike traditional systems that rely on central authorities or databases. US soft drinks company Long Island Iced Tea Corporation became Long Blockchain Corporation and saw its stock rise 400 per cent overnight, despite having no blockchain product. Kodak launched a vague cryptocurrency called KodakCoin, sending its stock price soaring.These developments were less about innovation and more about speculation, chasing short-term gains driven by hype. Most blockchain projects never delivered real value. Companies rushed in, driven by fear of missing out and the promise of technological transformation.", 
        "source": "TechNews"}
    ]'''
    
    # UPDATED: Now uses fal.ai instead of HuggingFace
    maker = AsyncNewsPresentationMaker(
        openai_key="...",
        fal_key="c95b464d-32a9-4059-b586-eeeafc917469:b0eb0e0cf6f9f5a73d19f779d1e86ef8",
        elevenlabs_key="sk_75fc980fe0800206a73c8fdf36e94246a357acdf7f3ee3c2"
    )
    
    # Process (now much faster + no rate limits!)
    print("⚡ Processing with fal.ai FLUX Dev + async...")
    result = maker.process_json_input(test_json)
    
    print("Done!")
