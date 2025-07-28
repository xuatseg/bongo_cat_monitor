#include <lvgl.h>
#include <TFT_eSPI.h>
#include <WiFi.h>
#include "Free_Fonts.h"
#include "animations_sprites.h"

// Display settings
#define SCREEN_WIDTH 240
#define SCREEN_HEIGHT 320

TFT_eSPI tft = TFT_eSPI();

// LVGL display buffer
static lv_disp_draw_buf_t draw_buf;
static lv_color_t buf[SCREEN_WIDTH * 10];

// Animation system with sprites
sprite_manager_t sprite_manager;
lv_obj_t * cat_canvas = NULL;
uint32_t last_frame_time = 0;
bool animation_paused = false;

// Enhanced animation control
bool python_control_mode = true;  // Python controls idle progression
uint32_t last_command_time = 0;   // Track when last command received
#define TYPING_TIMEOUT_MS 2000    // Stop typing animation after 2 seconds of no commands
#define PYTHON_TIMEOUT_MS 5000    // Fall back to auto mode after 5 seconds

// Simplified animation performance (removed aggressive frame limiting)
uint32_t frame_skip_counter = 0;

// Cat positioning (restored to original working method)
#define CAT_SIZE 64   // Base sprite size

// System stats display
lv_obj_t * screen = NULL;
lv_obj_t * cpu_label = NULL;
lv_obj_t * ram_label = NULL;
lv_obj_t * wpm_label = NULL;
lv_obj_t * time_label = NULL;

// Stats data
int cpu_usage = 0;
int ram_usage = 0;
int wpm_speed = 0;
String current_time_str = "00:00";
bool time_initialized = false;  // Track if we've received time from Python

// Function to flush the display buffer
void my_disp_flush(lv_disp_drv_t *disp, const lv_area_t *area, lv_color_t *color_p) {
    uint32_t w = (area->x2 - area->x1 + 1);
    uint32_t h = (area->y2 - area->y1 + 1);

    tft.startWrite();
    tft.setAddrWindow(area->x1, area->y1, w, h);
    tft.pushColors((uint16_t*)&color_p->full, w * h, true);
    tft.endWrite();

    lv_disp_flush_ready(disp);
}

// Update system stats display
void updateSystemStats(int cpu, int ram, int wpm) {
    cpu_usage = cpu;
    ram_usage = ram;
    wpm_speed = wpm;
    
    if (cpu_label) {
        lv_label_set_text_fmt(cpu_label, "CPU: %d%%", cpu);
    }
    if (ram_label) {
        lv_label_set_text_fmt(ram_label, "RAM: %d%%", ram);
    }
    if (wpm_label) {
        lv_label_set_text_fmt(wpm_label, "WPM: %d", wpm);
    }
}

// Update time display  
void updateTimeDisplay() {
    if (time_label && current_time_str.length() > 0) {
        lv_label_set_text(time_label, current_time_str.c_str());
        
        // Debug output for time updates
        if (!time_initialized) {
            Serial.print("🕐 Time initialized: ");
            Serial.println(current_time_str);
            time_initialized = true;
        }
    }
}

// Handle serial commands from Python script
void handleSerialCommands() {
    if (Serial.available()) {
        String command = Serial.readStringUntil('\n');
        command.trim();
        
        uint32_t current_time = millis();
        last_command_time = current_time;  // Update command timestamp
        python_control_mode = true;        // Ensure Python control is active
        
        if (command.startsWith("SPEED:")) {
            // Handle speed commands with enhanced logic  
            String speed_str = command.substring(6);
            uint16_t speed = speed_str.toInt();
            
            // Updated thresholds to match Python script (2024 industry standards)
            // Research shows: Average 40-45 WPM, Slow <20, Good 50-60, Professional 70+
            animation_state_t new_state = sprite_manager.current_state;
            
            if (speed == 0) {
                // Explicit stop command
                sprite_manager_set_state(&sprite_manager, ANIM_STATE_IDLE_STAGE1, current_time);
            } else if (speed < 80) {        // Slow threshold: <20 WPM -> speed 80+
                new_state = ANIM_STATE_TYPING_SLOW;
            } else if (speed < 150) {       // Normal threshold: 20-40 WPM -> speed 80-150
                new_state = ANIM_STATE_TYPING_NORMAL;
            } else {                        // Fast threshold: 40+ WPM -> speed 150+
                new_state = ANIM_STATE_TYPING_FAST;
            }
            
            // Always refresh state to prevent stuck animations (even if same state)
            sprite_manager_set_state(&sprite_manager, new_state, current_time);
            Serial.println("🔄 Animation state refreshed");
            
            // Check for significant speed changes that might cause stuck paws
            uint16_t old_speed = sprite_manager.animation_speed_ms;
            sprite_manager.animation_speed_ms = speed;
            
            // If speed changed significantly, reset paw timing to prevent stuck paws
            if (sprite_manager.paw_animation_active && abs((int)speed - (int)old_speed) > 50) {
                sprite_manager.paw_timer = current_time;  // Reset timing
                Serial.println("🔄 Speed change - resetting paw timing");
            }
            
            // Reset Python control timeout
            last_command_time = current_time;
            python_control_mode = true;
            sprite_manager.idle_progression_enabled = false;
        } else if (command == "STOP") {
            // Explicit stop command - better than IDLE
            sprite_manager_set_state(&sprite_manager, ANIM_STATE_IDLE_STAGE1, current_time);
            sprite_manager.idle_progression_enabled = false; // Keep disabled until IDLE_START
            python_control_mode = true;
            last_command_time = current_time;
            Serial.println("🛑 Received STOP command");
            
        } else if (command == "IDLE_START") {
            // Enable idle progression when Python detects no typing
            sprite_manager_set_state(&sprite_manager, ANIM_STATE_IDLE_STAGE1, current_time);
            sprite_manager.idle_progression_enabled = true;  // Enable automatic progression
            python_control_mode = false;  // Let Arduino handle idle progression
            Serial.println("😴 Idle progression enabled");
            
        } else if (command == "IDLE") {
            // Compatibility with old command
            sprite_manager_set_state(&sprite_manager, ANIM_STATE_IDLE_STAGE1, current_time);
            Serial.println("PONG");
            
        } else if (command == "HEARTBEAT") {
            // Connection keepalive - just reset timeout
            last_command_time = current_time;
            python_control_mode = true;
        } else if (command == "STREAK_ON") {
            // Enable streak mode (happy face)
            sprite_manager.is_streak_mode = true;
            Serial.println("😊 Streak mode enabled - happy face!");
        } else if (command == "STREAK_OFF") {
            // Disable streak mode
            sprite_manager.is_streak_mode = false;
            Serial.println("😐 Streak mode disabled - normal face");
        } else if (command.startsWith("STATS:")) {
            // Parse stats: STATS:CPU:45,RAM:67,WPM:23
            String stats = command.substring(6);
            
            int cpuStart = stats.indexOf("CPU:") + 4;
            int cpuEnd = stats.indexOf(",", cpuStart);
            int cpu = stats.substring(cpuStart, cpuEnd).toInt();
            
            int ramStart = stats.indexOf("RAM:") + 4;
            int ramEnd = stats.indexOf(",", ramStart);
            int ram = stats.substring(ramStart, ramEnd).toInt();
            
            int wpmStart = stats.indexOf("WPM:") + 4;
            int wpm = stats.substring(wpmStart).toInt();
            
            updateSystemStats(cpu, ram, wpm);
            
        } else if (command.startsWith("TIME:")) {
            // Handle time updates from Python script
            String time_str = command.substring(5);
            if (time_str.length() == 5 && time_str.charAt(2) == ':') {
                current_time_str = time_str;
            }
            
        } else if (command.startsWith("CPU:")) {
            // Handle CPU usage updates
            cpu_usage = command.substring(4).toInt();
            
        } else if (command.startsWith("RAM:")) {
            // Handle RAM usage updates  
            ram_usage = command.substring(4).toInt();
            
        } else if (command.startsWith("WPM:")) {
            // Handle WPM display updates
            wpm_speed = command.substring(4).toInt();
            
        } else if (command == "PING") {
            Serial.println("PONG");
            
        } else if (command.startsWith("ANIM:")) {
            // Handle specific animation commands from tester
            String anim = command.substring(5);
            if (anim == "IDLE_1") {
                sprite_manager_set_state(&sprite_manager, ANIM_STATE_IDLE_STAGE1, current_time);
            } else if (anim == "IDLE_2") {
                sprite_manager_set_state(&sprite_manager, ANIM_STATE_IDLE_STAGE2, current_time);
            } else if (anim == "IDLE_3") {
                sprite_manager_set_state(&sprite_manager, ANIM_STATE_IDLE_STAGE3, current_time);
            } else if (anim == "IDLE_4") {
                sprite_manager_set_state(&sprite_manager, ANIM_STATE_IDLE_STAGE4, current_time);
            } else if (anim == "BLINK") {
                sprite_manager_set_state(&sprite_manager, ANIM_STATE_BLINKING, current_time);
            } else if (anim == "EAR_TWITCH") {
                sprite_manager_set_state(&sprite_manager, ANIM_STATE_EAR_TWITCH, current_time);
            }
            Serial.println("PONG");
        }
    }
}

// Sprite management functions
void sprite_manager_init(sprite_manager_t* manager) {
    // Initialize all layers to basic state
    manager->current_sprites[LAYER_BODY] = &standardbody1;
    manager->current_sprites[LAYER_FACE] = &stock_face;
    manager->current_sprites[LAYER_TABLE] = &table1;
    manager->current_sprites[LAYER_PAWS] = &twopawsup;  // Default paws up
    manager->current_sprites[LAYER_EFFECTS] = NULL;
    
    manager->current_state = ANIM_STATE_IDLE_STAGE1;
    manager->state_start_time = millis();
    manager->blink_timer = millis() + random(3000, 8000);
    manager->ear_twitch_timer = millis() + random(10000, 30000);
    manager->effect_timer = 0;
    manager->effect_frame = 0;
    manager->paw_animation_active = false;
    manager->paw_frame = 0;
    manager->paw_timer = 0;
    manager->animation_speed_ms = 200;  // Default speed
    manager->click_effect_left = false;
    
    // Enhanced animation control
    manager->idle_progression_enabled = false;  // Start with Python control
    manager->last_typing_time = 0;
    manager->is_streak_mode = false;             // Start without streak mode
    
    // Initialize animation state variables
    manager->blink_start_time = 0;
    manager->blinking = false;
    manager->ear_twitch_start_time = 0;
    manager->ear_twitching = false;
    
    Serial.println("🐱 Sprite manager initialized");
}

void sprite_manager_update(sprite_manager_t* manager, uint32_t current_time) {
    // Check for typing timeout (Arduino-side safety)
    if (manager->paw_animation_active && manager->last_typing_time > 0) {
        if (current_time - manager->last_typing_time > TYPING_TIMEOUT_MS) {
            // Stop typing animation due to timeout
            manager->paw_animation_active = false;
            manager->current_sprites[LAYER_EFFECTS] = NULL;
            Serial.println("🛑 Typing timeout - stopping animation");
        }
    }
    
    // Check if Python control has timed out
    if (python_control_mode && current_time - last_command_time > PYTHON_TIMEOUT_MS) {
        python_control_mode = false;
        manager->idle_progression_enabled = true;
        Serial.println("⚠️ Python timeout - enabling auto mode");
    }
    
    // Handle automatic idle progression only if enabled
    if (manager->idle_progression_enabled || !python_control_mode) {
        if (manager->current_state == ANIM_STATE_IDLE_STAGE1) {
            if (current_time - manager->state_start_time > 3000) { // 3 seconds
                sprite_manager_set_state(manager, ANIM_STATE_IDLE_STAGE2, current_time);
            }
        } else if (manager->current_state == ANIM_STATE_IDLE_STAGE2) {
            if (current_time - manager->state_start_time > 5000) { // 5 seconds  
                sprite_manager_set_state(manager, ANIM_STATE_IDLE_STAGE3, current_time);
            }
        } else if (manager->current_state == ANIM_STATE_IDLE_STAGE3) {
            if (current_time - manager->state_start_time > 7000) { // 7 seconds
                sprite_manager_set_state(manager, ANIM_STATE_IDLE_STAGE4, current_time);
            }
        }
    }
    
    // Handle paw animations - 4-step pattern: left_down → both_up → right_down → both_up
    if (manager->paw_animation_active) {
        // Trust Python's speed calculations - no additional rate limiting
        if (current_time - manager->paw_timer >= manager->animation_speed_ms) {
            manager->paw_frame = (manager->paw_frame + 1) % 4;  // 4-step pattern
            
            // 4-step typing pattern with effects synchronized to paw strikes
            switch (manager->paw_frame) {
                case 0:  // Left paw down
                    manager->current_sprites[LAYER_PAWS] = &leftpawdown;
                    // Show left click effect for fast typing
                    if (manager->current_state == ANIM_STATE_TYPING_FAST || 
                        manager->current_state == ANIM_STATE_TYPING_STREAK) {
                        manager->current_sprites[LAYER_EFFECTS] = &left_click_effect;
                    } else {
                        manager->current_sprites[LAYER_EFFECTS] = NULL;
                    }
                    break;
                    
                case 1:  // Both paws up (rest position)
                    manager->current_sprites[LAYER_PAWS] = &twopawsup;
                    manager->current_sprites[LAYER_EFFECTS] = NULL;  // No effects during rest
                    break;
                    
                case 2:  // Right paw down  
                    manager->current_sprites[LAYER_PAWS] = &rightpawdown;
                    // Show right click effect for fast typing
                    if (manager->current_state == ANIM_STATE_TYPING_FAST || 
                        manager->current_state == ANIM_STATE_TYPING_STREAK) {
                        manager->current_sprites[LAYER_EFFECTS] = &right_click_effect;
                    } else {
                        manager->current_sprites[LAYER_EFFECTS] = NULL;
                    }
                    break;
                    
                case 3:  // Both paws up (rest position)
                    manager->current_sprites[LAYER_PAWS] = &twopawsup;
                    manager->current_sprites[LAYER_EFFECTS] = NULL;  // No effects during rest
                    break;
            }
            manager->paw_timer = current_time;
        }
    } else {
        // When not typing, ensure paws are in the correct idle position based on state
        if (manager->current_state == ANIM_STATE_IDLE_STAGE1) {
            manager->current_sprites[LAYER_PAWS] = &twopawsup;  // Visible paws for stage 1
        } else if (manager->current_state >= ANIM_STATE_IDLE_STAGE2 && 
                   manager->current_state <= ANIM_STATE_IDLE_STAGE4) {
            manager->current_sprites[LAYER_PAWS] = NULL;  // Hidden paws for stages 2-4
        }
        
        // Only clear effects if NOT in IDLE_STAGE4 (which needs sleepy effects)
        if (manager->current_state != ANIM_STATE_IDLE_STAGE4) {
            manager->current_sprites[LAYER_EFFECTS] = NULL;  // Clear typing effects
        }
    }
    
    // Handle sleepy effects animation (for IDLE_STAGE4)
    if (manager->current_state == ANIM_STATE_IDLE_STAGE4) {
        if (current_time - manager->effect_timer > 1000) { // Change effect every second
            manager->effect_frame = (manager->effect_frame + 1) % 3;
            switch (manager->effect_frame) {
                case 0: manager->current_sprites[LAYER_EFFECTS] = &sleepy1; break;
                case 1: manager->current_sprites[LAYER_EFFECTS] = &sleepy2; break;
                case 2: manager->current_sprites[LAYER_EFFECTS] = &sleepy3; break;
            }
            manager->effect_timer = current_time;
        }
    }
    
    // Handle automatic blinking (only when awake, not during sleep)
    // Only blink when not sleeping (stages 3 and 4 have sleepy face, no blinking)
    bool can_blink = (manager->current_state != ANIM_STATE_IDLE_STAGE3 && 
                      manager->current_state != ANIM_STATE_IDLE_STAGE4);
    
    if (!manager->blinking && current_time >= manager->blink_timer && can_blink) {
        // Start blink
        manager->blinking = true;
        manager->blink_start_time = current_time;
        manager->current_sprites[LAYER_FACE] = &blink_face;
    } else if (manager->blinking && current_time - manager->blink_start_time > 200) {
        // End blink after 200ms
        manager->blinking = false;
        // Restore normal face after blink based on current state and streak mode
        if (manager->current_state == ANIM_STATE_IDLE_STAGE3 || 
            manager->current_state == ANIM_STATE_IDLE_STAGE4) {
            manager->current_sprites[LAYER_FACE] = &sleepy_face;
        } else if (manager->is_streak_mode && manager->paw_animation_active) {
            manager->current_sprites[LAYER_FACE] = &happy_face;  // Happy face during any typing streak
        } else {
            manager->current_sprites[LAYER_FACE] = &stock_face;  // Default face
        }
        // Set next blink time (only if can still blink)
        if (can_blink) {
            manager->blink_timer = current_time + random(3000, 8000);
        } else {
            // When entering sleep, set longer blink timer for when waking up
            manager->blink_timer = current_time + random(5000, 10000);
        }
    }
    
    // Handle ear twitch
    if (!manager->ear_twitching && current_time >= manager->ear_twitch_timer) {
        // Start ear twitch
        manager->ear_twitching = true;
        manager->ear_twitch_start_time = current_time;
        manager->current_sprites[LAYER_BODY] = &bodyeartwitch;
    } else if (manager->ear_twitching && current_time - manager->ear_twitch_start_time > 500) {
        // End ear twitch after 500ms
        manager->ear_twitching = false;
        manager->current_sprites[LAYER_BODY] = &standardbody1;
        // Set next ear twitch time
        manager->ear_twitch_timer = current_time + random(10000, 30000);
    }
}

void sprite_manager_set_state(sprite_manager_t* manager, animation_state_t new_state, uint32_t current_time) {
    Serial.print("🔄 Animation state: ");
    Serial.print(get_state_name(manager->current_state));
    Serial.print(" → ");
    Serial.println(get_state_name(new_state));
    
    manager->current_state = new_state;
    manager->state_start_time = current_time;
    
    // Update typing timing for timeout tracking
    if (new_state == ANIM_STATE_TYPING_SLOW || 
        new_state == ANIM_STATE_TYPING_NORMAL || 
        new_state == ANIM_STATE_TYPING_FAST) {
        manager->last_typing_time = current_time;
    }
    
    // Set appropriate sprites based on state - always ensure base layers are set
    // Base layers that should always be present
    manager->current_sprites[LAYER_BODY] = &standardbody1;
    manager->current_sprites[LAYER_TABLE] = &table1;
    
    switch (new_state) {
        case ANIM_STATE_IDLE_STAGE1:
            // Stage 1: Stock face with paws up (hands visible above table)
            manager->current_sprites[LAYER_PAWS] = &twopawsup;  // Both paws visible above table
            manager->current_sprites[LAYER_EFFECTS] = NULL;
            manager->current_sprites[LAYER_FACE] = &stock_face;
            manager->paw_animation_active = false;
            Serial.println("😐 Stage 1: Stock face, paws up");
            break;
            
        case ANIM_STATE_IDLE_STAGE2:
            // Stage 2: Stock face + hands gone (underneath table)
            manager->current_sprites[LAYER_PAWS] = NULL;  // No paws visible (hands underneath table)
            manager->current_sprites[LAYER_EFFECTS] = NULL;
            manager->current_sprites[LAYER_FACE] = &stock_face;  // Still stock face
            manager->paw_animation_active = false;
            Serial.println("😐 Stage 2: Stock face, hands hidden");
            break;
            
        case ANIM_STATE_IDLE_STAGE3:
            // Stage 3: Hands gone + sleepy face (prepare for effects)
            manager->current_sprites[LAYER_PAWS] = NULL;  // No paws visible
            manager->current_sprites[LAYER_EFFECTS] = NULL;
            manager->current_sprites[LAYER_FACE] = &sleepy_face;
            manager->paw_animation_active = false;
            Serial.println("😴 Stage 3: Deep sleep preparation, hands hidden");
            break;
            
        case ANIM_STATE_IDLE_STAGE4:
            // Stage 4: Hands gone + sleepy face + cycling sleepy effects
            manager->current_sprites[LAYER_PAWS] = NULL;  // No paws visible
            manager->current_sprites[LAYER_FACE] = &sleepy_face;
            manager->paw_animation_active = false;
            manager->effect_timer = current_time;  // Initialize effect timer for cycling
            // Effects will cycle in main update loop
            Serial.println("😴 Stage 4: Deep sleep with cycling effects, hands hidden");
            break;
            
        case ANIM_STATE_TYPING_SLOW:
            // Slow typing: 4-step paw pattern, no effects
            manager->current_sprites[LAYER_FACE] = manager->is_streak_mode ? &happy_face : &stock_face;
            manager->current_sprites[LAYER_EFFECTS] = NULL;
            manager->current_sprites[LAYER_PAWS] = &leftpawdown;  // Start with left paw (frame 0)
            manager->paw_animation_active = true;
            manager->paw_frame = 0;  // Reset paw frame to prevent stuck paws
            manager->paw_timer = current_time;
            Serial.println(manager->is_streak_mode ? "👐😊 Slow typing with happy face" : "👐 Slow typing");
            break;
            
        case ANIM_STATE_TYPING_NORMAL:
            // Normal typing: 4-step paw pattern, no effects
            manager->current_sprites[LAYER_FACE] = manager->is_streak_mode ? &happy_face : &stock_face;
            manager->current_sprites[LAYER_EFFECTS] = NULL;
            manager->current_sprites[LAYER_PAWS] = &leftpawdown;  // Start with left paw (frame 0)
            manager->paw_animation_active = true;
            manager->paw_frame = 0;  // Reset paw frame to prevent stuck paws
            manager->paw_timer = current_time;
            Serial.println(manager->is_streak_mode ? "👐😊 Normal typing with happy face" : "👐 Normal typing");
            break;
            
        case ANIM_STATE_TYPING_FAST:
            // Fast typing: 4-step paw pattern + click effects
            manager->current_sprites[LAYER_FACE] = manager->is_streak_mode ? &happy_face : &stock_face;
            manager->current_sprites[LAYER_PAWS] = &leftpawdown;  // Start with left paw (frame 0)
            manager->paw_animation_active = true;
            manager->paw_frame = 0;  // Reset paw frame to prevent stuck paws
            manager->paw_timer = current_time;
            Serial.println(manager->is_streak_mode ? "👐⚡😊 Fast typing with happy face and effects" : "👐⚡ Fast typing with click effects");
            break;
            
        case ANIM_STATE_TYPING_STREAK:
            // Legacy streak state - treat as fast typing with happy face
            manager->current_sprites[LAYER_FACE] = &happy_face;
            manager->current_sprites[LAYER_PAWS] = &leftpawdown;  // Start with left paw (frame 0)
            manager->paw_animation_active = true;
            manager->paw_frame = 0;  // Reset paw frame to prevent stuck paws
            manager->paw_timer = current_time;
            Serial.println("👐⚡😊 Legacy streak mode - fast typing with happy face");
            break;
    }
    
    // Reset idle progression when entering any typing state
    if (new_state == ANIM_STATE_TYPING_SLOW || 
        new_state == ANIM_STATE_TYPING_NORMAL || 
        new_state == ANIM_STATE_TYPING_FAST) {
        manager->idle_progression_enabled = false;  // Stop auto idle progression
        Serial.println("🚫 Auto idle progression disabled");
    }
}

void sprite_render_layers(sprite_manager_t* manager, lv_obj_t* canvas, uint32_t current_time) {
    // Clear canvas with minimal operations
    lv_canvas_fill_bg(canvas, lv_color_white(), LV_OPA_TRANSP);
    
    // Render layers in order (back to front) with optimized drawing
    lv_draw_img_dsc_t img_dsc;
    lv_draw_img_dsc_init(&img_dsc);  // Initialize once outside loop
    
    for (int layer = 0; layer < NUM_LAYERS; layer++) {
        const lv_img_dsc_t* sprite = manager->current_sprites[layer];
        if (sprite) {
            // Draw sprite at origin (0,0) - canvas will be zoomed to 4x size
            // Using single draw call per sprite to minimize operations
            lv_canvas_draw_img(canvas, 0, 0, sprite, &img_dsc);
        }
    }
}

// Helper function to get state name for debugging
const char* get_state_name(animation_state_t state) {
    switch (state) {
        case ANIM_STATE_IDLE_STAGE1: return "IDLE_STAGE1";
        case ANIM_STATE_IDLE_STAGE2: return "IDLE_STAGE2"; 
        case ANIM_STATE_IDLE_STAGE3: return "IDLE_STAGE3";
        case ANIM_STATE_IDLE_STAGE4: return "IDLE_STAGE4";
        case ANIM_STATE_TYPING_SLOW: return "TYPING_SLOW";
        case ANIM_STATE_TYPING_NORMAL: return "TYPING_NORMAL";
        case ANIM_STATE_TYPING_FAST: return "TYPING_FAST";
        case ANIM_STATE_TYPING_STREAK: return "TYPING_STREAK";  // Keep for compatibility but unused
        default: return "UNKNOWN";
    }
}

void setup() {
    Serial.begin(115200);
    Serial.println("🐱 Bongo Cat with Sprites Starting...");
    
    // Initialize random seed for animations
    randomSeed(analogRead(0));
    
    tft.init();
    tft.setRotation(0);
    tft.fillScreen(TFT_WHITE);  // White background
    
    lv_init();
    
    lv_disp_draw_buf_init(&draw_buf, buf, NULL, SCREEN_WIDTH * 10);
    
    static lv_disp_drv_t disp_drv;
    lv_disp_drv_init(&disp_drv);
    disp_drv.hor_res = SCREEN_WIDTH;
    disp_drv.ver_res = SCREEN_HEIGHT;
    disp_drv.flush_cb = my_disp_flush;
    disp_drv.draw_buf = &draw_buf;
    lv_disp_drv_register(&disp_drv);
    
    // Initialize sprite manager
    sprite_manager_init(&sprite_manager);
    
    createBongoCat();
    
    Serial.println("✅ Bongo Cat Ready!");
}

void createBongoCat() {
    screen = lv_scr_act();
    
    // Set white background
    lv_obj_set_style_bg_color(screen, lv_color_white(), 0);
    
    // Create cat canvas with proper sizing
    cat_canvas = lv_canvas_create(screen);
    
    // Use 64x64 base sprite size for the canvas buffer
    static lv_color_t canvas_buf[CAT_SIZE * CAT_SIZE];  // 64x64 buffer
    lv_canvas_set_buffer(cat_canvas, canvas_buf, CAT_SIZE, CAT_SIZE, LV_IMG_CF_TRUE_COLOR);
    
    // Apply 4x zoom to make 64x64 sprites appear as 256x256 on screen
    lv_img_set_zoom(cat_canvas, 1024);  // 4x zoom: 64x64 -> 256x256 pixels
    lv_img_set_antialias(cat_canvas, false);  // Keep pixels crisp and blocky
    
    // Position cat: original alignment method + 3 cat pixels right + a bit lower
    lv_obj_align(cat_canvas, LV_ALIGN_CENTER, 12, 50);  // 12px right (3 cat pixels), 50px lower
    
    // Create system stats labels (top left) with pixelated font
    cpu_label = lv_label_create(screen);
    lv_label_set_text(cpu_label, "CPU: 0%");
    lv_obj_set_style_text_font(cpu_label, &lv_font_unscii_16, 0);
    lv_obj_set_style_text_color(cpu_label, lv_color_black(), 0);
    lv_obj_align(cpu_label, LV_ALIGN_TOP_LEFT, 5, 5);
    
    ram_label = lv_label_create(screen);
    lv_label_set_text(ram_label, "RAM: 0%");
    lv_obj_set_style_text_font(ram_label, &lv_font_unscii_16, 0);
    lv_obj_set_style_text_color(ram_label, lv_color_black(), 0);
    lv_obj_align(ram_label, LV_ALIGN_TOP_LEFT, 5, 25);
    
    wpm_label = lv_label_create(screen);
    lv_label_set_text(wpm_label, "WPM: 0");
    lv_obj_set_style_text_font(wpm_label, &lv_font_unscii_16, 0);
    lv_obj_set_style_text_color(wpm_label, lv_color_black(), 0);
    lv_obj_align(wpm_label, LV_ALIGN_TOP_LEFT, 5, 45);
    
    // Create time label (top right) - bigger pixelated font
    time_label = lv_label_create(screen);
    lv_label_set_text(time_label, "00:00");
    lv_obj_set_style_text_font(time_label, &lv_font_unscii_16, 0);
    lv_obj_set_style_text_color(time_label, lv_color_black(), 0);
    lv_obj_align(time_label, LV_ALIGN_TOP_RIGHT, -5, 5);
    
    // Initial render
    sprite_render_layers(&sprite_manager, cat_canvas, millis());
}

void loop() {
    handleSerialCommands();
    
    uint32_t current_time = millis();
    
    // Update animations - removed fixed frame rate to prevent conflicts
    static uint32_t last_animation_update = 0;
    if (current_time - last_animation_update >= 25) {  // 40 FPS max (more responsive)
        sprite_manager_update(&sprite_manager, current_time);
        
        // Only render if sprites actually changed to reduce canvas operations
        static uint32_t last_sprite_hash = 0;
        uint32_t current_sprite_hash = 0;
        
        // Calculate simple hash of current sprites to detect changes (optimized)
        for (int i = 0; i < NUM_LAYERS; i++) {
            current_sprite_hash += (uint32_t)sprite_manager.current_sprites[i];
        }
        
        // Only re-render if sprites changed or it's been too long (forced refresh)
        if (current_sprite_hash != last_sprite_hash || (current_time - last_animation_update) > 200) {
            sprite_render_layers(&sprite_manager, cat_canvas, current_time);
            last_sprite_hash = current_sprite_hash;
        }
        
        last_animation_update = current_time;
    }
    
    // Update time display every second
    static uint32_t last_time_update = 0;
    if (current_time - last_time_update >= 1000) {
        updateTimeDisplay();
        last_time_update = current_time;
    }
    
    // Reduce LVGL timer handler frequency to prevent system overload
    static uint32_t last_lvgl_update = 0;
    if (current_time - last_lvgl_update >= 20) {  // 50 FPS max for LVGL (was every 5ms)
        lv_timer_handler();
        last_lvgl_update = current_time;
    }
    
    delay(2);  // Reduced from 5ms for better responsiveness
} 