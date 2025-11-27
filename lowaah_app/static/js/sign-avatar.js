/**
 * 3D Sign Language Avatar System
 * Renders sign language animations using Three.js
 * 
 * Features:
 * - 3D humanoid avatar
 * - Hand pose animations
 * - Real-time rendering
 * - Fallback to video/images
 */

class SignLanguageAvatar {
    constructor(containerId) {
        this.container = document.getElementById(containerId);
        
        if (!this.container) {
            console.error(`Container ${containerId} not found`);
            return;
        }
        
        // Check if Three.js is available
        this.use3D = typeof THREE !== 'undefined';
        
        if (this.use3D) {
            this.init3DAvatar();
        } else {
            console.warn('Three.js not available, using fallback mode');
            this.initFallbackMode();
        }
        
        // Animation state
        this.currentAnimation = null;
        this.isPlaying = false;
        this.animationQueue = [];
        
        console.log('✅ SignLanguageAvatar initialized');
    }
    
    /**
     * Initialize 3D avatar using Three.js
     */
    init3DAvatar() {
        const width = this.container.clientWidth;
        const height = this.container.clientHeight || 400;
        
        // Create scene
        this.scene = new THREE.Scene();
        this.scene.background = new THREE.Color(0xf0f0f0);
        
        // Create camera
        this.camera = new THREE.PerspectiveCamera(50, width / height, 0.1, 1000);
        this.camera.position.set(0, 1.6, 3);
        this.camera.lookAt(0, 1.2, 0);
        
        // Create renderer
        this.renderer = new THREE.WebGLRenderer({ antialias: true });
        this.renderer.setSize(width, height);
        this.renderer.setPixelRatio(window.devicePixelRatio);
        this.renderer.shadowMap.enabled = true;
        this.container.appendChild(this.renderer.domElement);
        
        // Add lights
        this.addLights();
        
        // Create simple avatar (placeholder - would be replaced with detailed model)
        this.createSimpleAvatar();
        
        // Start render loop
        this.animate();
        
        // Handle window resize
        window.addEventListener('resize', () => this.onWindowResize());
        
        console.log('✅ 3D Avatar initialized');
    }
    
    /**
     * Add lighting to scene
     */
    addLights() {
        // Ambient light
        const ambientLight = new THREE.AmbientLight(0xffffff, 0.6);
        this.scene.add(ambientLight);
        
        // Directional light (sun)
        const dirLight = new THREE.DirectionalLight(0xffffff, 0.8);
        dirLight.position.set(5, 10, 5);
        dirLight.castShadow = true;
        this.scene.add(dirLight);
        
        // Fill light
        const fillLight = new THREE.DirectionalLight(0xffffff, 0.3);
        fillLight.position.set(-5, 5, -5);
        this.scene.add(fillLight);
    }
    
    /**
     * Create simple humanoid avatar (placeholder)
     * In production, load a detailed GLTF model
     */
    createSimpleAvatar() {
        this.avatar = new THREE.Group();
        
        // Body
        const bodyGeometry = new THREE.CylinderGeometry(0.3, 0.25, 0.8, 8);
        const bodyMaterial = new THREE.MeshPhongMaterial({ color: 0x4a90e2 });
        const body = new THREE.Mesh(bodyGeometry, bodyMaterial);
        body.position.y = 1.0;
        body.castShadow = true;
        this.avatar.add(body);
        
        // Head
        const headGeometry = new THREE.SphereGeometry(0.2, 16, 16);
        const headMaterial = new THREE.MeshPhongMaterial({ color: 0xfdbcb4 });
        const head = new THREE.Mesh(headGeometry, headMaterial);
        head.position.y = 1.6;
        head.castShadow = true;
        this.avatar.add(head);
        
        // Arms (simplified)
        this.createArm('left', -0.4);
        this.createArm('right', 0.4);
        
        // Ground plane
        const groundGeometry = new THREE.PlaneGeometry(10, 10);
        const groundMaterial = new THREE.MeshPhongMaterial({ color: 0xcccccc });
        const ground = new THREE.Mesh(groundGeometry, groundMaterial);
        ground.rotation.x = -Math.PI / 2;
        ground.receiveShadow = true;
        this.scene.add(ground);
        
        this.scene.add(this.avatar);
    }
    
    /**
     * Create avatar arm
     */
    createArm(side, xOffset) {
        const armGroup = new THREE.Group();
        
        // Upper arm
        const upperArmGeometry = new THREE.CylinderGeometry(0.08, 0.07, 0.4, 8);
        const armMaterial = new THREE.MeshPhongMaterial({ color: 0xfdbcb4 });
        const upperArm = new THREE.Mesh(upperArmGeometry, armMaterial);
        upperArm.position.set(xOffset, 1.2, 0);
        upperArm.castShadow = true;
        
        // Lower arm
        const lowerArm = new THREE.Mesh(upperArmGeometry, armMaterial);
        lowerArm.position.set(0, -0.4, 0);
        lowerArm.castShadow = true;
        upperArm.add(lowerArm);
        
        // Hand (simplified)
        const handGeometry = new THREE.BoxGeometry(0.12, 0.15, 0.05);
        const hand = new THREE.Mesh(handGeometry, armMaterial);
        hand.position.set(0, -0.3, 0);
        hand.castShadow = true;
        lowerArm.add(hand);
        
        // Store references
        if (side === 'left') {
            this.leftArm = upperArm;
            this.leftHand = hand;
        } else {
            this.rightArm = upperArm;
            this.rightHand = hand;
        }
        
        armGroup.add(upperArm);
        this.avatar.add(armGroup);
    }
    
    /**
     * Animation loop
     */
    animate() {
        requestAnimationFrame(() => this.animate());
        
        // Render scene
        this.renderer.render(this.scene, this.camera);
    }
    
    /**
     * Handle window resize
     */
    onWindowResize() {
        const width = this.container.clientWidth;
        const height = this.container.clientHeight || 400;
        
        this.camera.aspect = width / height;
        this.camera.updateProjectionMatrix();
        this.renderer.setSize(width, height);
    }
    
    /**
     * Play sign language animation
     * @param {Object} animationData - Animation data from backend
     */
    async playAnimation(animationData) {
        if (!animationData || !animationData.signs) {
            console.error('Invalid animation data');
            return;
        }
        
        console.log('🎬 Playing animation:', animationData.text);
        this.isPlaying = true;
        
        for (const sign of animationData.signs) {
            if (!this.isPlaying) break;
            
            await this.playSign(sign);
        }
        
        this.isPlaying = false;
        console.log('✅ Animation complete');
    }
    
    /**
     * Play individual sign
     */
    async playSign(sign) {
        return new Promise((resolve) => {
            const duration = sign.end_time - sign.start_time;
            
            // Display text subtitle
            this.showSubtitle(sign.display_text);
            
            if (this.use3D && sign.animation) {
                // Animate 3D avatar
                this.animate3DSign(sign.animation);
            }
            
            // Wait for duration
            setTimeout(() => {
                resolve();
            }, duration * 1000);
        });
    }
    
    /**
     * Animate 3D avatar for a sign
     */
    animate3DSign(animationData) {
        if (!animationData || !animationData.keyframes) return;
        
        const keyframes = animationData.keyframes;
        
        // Simple animation (would use GSAP or Three.js animation mixer in production)
        keyframes.forEach((keyframe, index) => {
            setTimeout(() => {
                this.applyKeyframe(keyframe);
            }, keyframe.time * 1000);
        });
    }
    
    /**
     * Apply keyframe to avatar
     */
    applyKeyframe(keyframe) {
        const hand = keyframe.hand === 'left' ? this.leftHand : this.rightHand;
        const arm = keyframe.hand === 'left' ? this.leftArm : this.rightArm;
        
        if (!hand || !arm) return;
        
        // Animate to position
        const targetPos = new THREE.Vector3(...keyframe.position);
        const targetRot = new THREE.Euler(
            keyframe.rotation[0] * Math.PI / 180,
            keyframe.rotation[1] * Math.PI / 180,
            keyframe.rotation[2] * Math.PI / 180
        );
        
        // Simple lerp animation (would use Tween.js in production)
        this.animateTransform(arm, targetPos, targetRot, 0.5);
    }
    
    /**
     * Animate transform with lerp
     */
    animateTransform(object, targetPos, targetRot, duration) {
        const startPos = object.position.clone();
        const startRot = object.rotation.clone();
        const startTime = Date.now();
        
        const animate = () => {
            const elapsed = (Date.now() - startTime) / 1000;
            const progress = Math.min(elapsed / duration, 1);
            
            // Lerp position
            object.position.lerpVectors(startPos, targetPos, progress);
            
            // Lerp rotation
            object.rotation.x = startRot.x + (targetRot.x - startRot.x) * progress;
            object.rotation.y = startRot.y + (targetRot.y - startRot.y) * progress;
            object.rotation.z = startRot.z + (targetRot.z - startRot.z) * progress;
            
            if (progress < 1) {
                requestAnimationFrame(animate);
            }
        };
        
        animate();
    }
    
    /**
     * Show subtitle text
     */
    showSubtitle(text) {
        let subtitle = document.getElementById('sign-subtitle');
        
        if (!subtitle) {
            subtitle = document.createElement('div');
            subtitle.id = 'sign-subtitle';
            subtitle.style.cssText = `
                position: absolute;
                bottom: 20px;
                left: 50%;
                transform: translateX(-50%);
                background: rgba(0, 0, 0, 0.7);
                color: white;
                padding: 10px 20px;
                border-radius: 5px;
                font-size: 18px;
                font-weight: bold;
                z-index: 100;
            `;
            this.container.appendChild(subtitle);
        }
        
        subtitle.textContent = text;
        subtitle.style.display = 'block';
        
        // Hide after duration
        setTimeout(() => {
            if (subtitle) subtitle.style.display = 'none';
        }, 1200);
    }
    
    /**
     * Initialize fallback mode (images/video)
     */
    initFallbackMode() {
        this.fallbackContainer = document.createElement('div');
        this.fallbackContainer.className = 'sign-fallback-container';
        this.fallbackContainer.style.cssText = `
            width: 100%;
            height: 400px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #f0f0f0;
            position: relative;
        `;
        
        this.fallbackImage = document.createElement('img');
        this.fallbackImage.style.cssText = `
            max-width: 80%;
            max-height: 80%;
            object-fit: contain;
        `;
        
        this.fallbackContainer.appendChild(this.fallbackImage);
        this.container.appendChild(this.fallbackContainer);
        
        console.log('✅ Fallback mode initialized');
    }
    
    /**
     * Play animation in fallback mode
     */
    async playAnimationFallback(animationData) {
        console.log('🎬 Playing fallback animation:', animationData.text);
        
        for (const sign of animationData.signs) {
            await this.playSignFallback(sign);
        }
        
        console.log('✅ Fallback animation complete');
    }
    
    /**
     * Play sign in fallback mode (image)
     */
    async playSignFallback(sign) {
        return new Promise((resolve) => {
            const duration = sign.end_time - sign.start_time;
            
            // Show sign image
            const imagePath = this.getSignImagePath(sign);
            this.fallbackImage.src = imagePath;
            
            // Show subtitle
            this.showSubtitle(sign.display_text);
            
            setTimeout(() => {
                resolve();
            }, duration * 1000);
        });
    }
    
    /**
     * Get image path for sign
     */
    getSignImagePath(sign) {
        // Return path to static sign images
        const type = sign.type;
        const text = sign.display_text || '';
        
        if (type === 'letter') {
            return `/static/signs/letters/${text}.png`;
        } else if (type === 'word') {
            return `/static/signs/words/${text}.png`;
        } else if (type === 'number') {
            return `/static/signs/numbers/${text}.png`;
        }
        
        return `/static/signs/placeholder.png`;
    }
    
    /**
     * Stop current animation
     */
    stop() {
        this.isPlaying = false;
        this.animationQueue = [];
    }
    
    /**
     * Reset avatar to default pose
     */
    reset() {
        if (this.use3D) {
            // Reset arms to default position
            if (this.leftArm) {
                this.leftArm.position.set(-0.4, 1.2, 0);
                this.leftArm.rotation.set(0, 0, 0);
            }
            if (this.rightArm) {
                this.rightArm.position.set(0.4, 1.2, 0);
                this.rightArm.rotation.set(0, 0, 0);
            }
        }
    }
}

// Export for use in other scripts
window.SignLanguageAvatar = SignLanguageAvatar;


