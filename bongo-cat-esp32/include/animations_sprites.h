#ifndef ANIMATIONS_SPRITES_H
#define ANIMATIONS_SPRITES_H

// Include LVGL for image descriptor types
#ifdef __has_include
    #if __has_include("lvgl.h")
        #ifndef LV_LVGL_H_INCLUDE_SIMPLE
            #define LV_LVGL_H_INCLUDE_SIMPLE
        #endif
    #endif
#endif

#if defined(LV_LVGL_H_INCLUDE_SIMPLE)
    #include "lvgl.h"
#else
    #include "lvgl/lvgl.h"
#endif

// Body sprites
#include "../lib/bongo_cat_animations/src/body/standardbody1.c"
#include "../lib/bongo_cat_animations/src/body/bodyeartwitch.c"

// Face sprites  
#include "../lib/bongo_cat_animations/src/faces/stock_face.c"
#include "../lib/bongo_cat_animations/src/faces/happy_face.c"
#include "../lib/bongo_cat_animations/src/faces/blink_face.c"
#include "../lib/bongo_cat_animations/src/faces/sleepy_face.c"

// Paw sprites
#include "../lib/bongo_cat_animations/src/paws/leftpawdown.c"
#include "../lib/bongo_cat_animations/src/paws/rightpawdown.c"
#include "../lib/bongo_cat_animations/src/paws/twopawsup.c"

// Table sprites
#include "../lib/bongo_cat_animations/src/table/table1.c"

// Effect sprites
#include "../lib/bongo_cat_animations/src/effects/left_click_effect.c"
#include "../lib/bongo_cat_animations/src/effects/right_click_effect.c"
#include "../lib/bongo_cat_animations/src/effects/sleepy1.c"
#include "../lib/bongo_cat_animations/src/effects/sleepy2.c"
#include "../lib/bongo_cat_animations/src/effects/sleepy3.c"

// External declarations for all sprites
extern const lv_img_dsc_t standardbody1;
extern const lv_img_dsc_t bodyeartwitch;
extern const lv_img_dsc_t stock_face;
extern const lv_img_dsc_t happy_face;
extern const lv_img_dsc_t blink_face;
extern const lv_img_dsc_t sleepy_face;
extern const lv_img_dsc_t leftpawdown;
extern const lv_img_dsc_t rightpawdown;
extern const lv_img_dsc_t twopawsup;
extern const lv_img_dsc_t table1;
extern const lv_img_dsc_t left_click_effect;
extern const lv_img_dsc_t right_click_effect;
extern const lv_img_dsc_t sleepy1;
extern const lv_img_dsc_t sleepy2;
extern const lv_img_dsc_t sleepy3;

// Sprite layer definitions (Z-order from back to front)
typedef enum {
    LAYER_BODY = 0,
    LAYER_FACE,
    LAYER_TABLE, 
    LAYER_PAWS,
    LAYER_EFFECTS,
    NUM_LAYERS
} sprite_layer_t;

// Animation state definitions
typedef enum {
    ANIM_STATE_IDLE_STAGE1 = 0,     // Paws up, all stock
    ANIM_STATE_IDLE_STAGE2,         // No paws, all stock  
    ANIM_STATE_IDLE_STAGE3,         // Sleepy face, no paws
    ANIM_STATE_IDLE_STAGE4,         // Sleepy face + effects
    ANIM_STATE_TYPING_SLOW,         // Stock face, slow paws
    ANIM_STATE_TYPING_NORMAL,       // Stock face, normal paws
    ANIM_STATE_TYPING_FAST,         // Stock face, fast paws + click effects
    ANIM_STATE_TYPING_STREAK,       // Happy face, ultra-fast paws
    ANIM_STATE_BLINKING,            // Brief blink animation
    ANIM_STATE_EAR_TWITCH           // Body sprite swap
} animation_state_t;

// Sprite management structure
typedef struct {
    const lv_img_dsc_t* current_sprites[NUM_LAYERS];
    animation_state_t current_state;
    uint32_t state_start_time;
    uint32_t blink_timer;
    uint32_t ear_twitch_timer;
    uint32_t effect_timer;
    uint8_t effect_frame;           // For sleepy effect animation (0,1,2)
    bool paw_animation_active;
    uint8_t paw_frame;              // Now 0-3 for 4-step typing pattern
    uint32_t paw_timer;
    uint16_t animation_speed_ms;
    bool click_effect_left;         // For alternating click effects
    
    // Enhanced animation control
    bool idle_progression_enabled;  // Allow automatic idle progression
    uint32_t last_typing_time;      // Track last typing command for timeout
    bool is_streak_mode;            // Flag for happy face during typing streak
    
    // Animation state variables (moved from static to prevent timing issues)
    uint32_t blink_start_time;      // When current blink started
    bool blinking;                  // Currently blinking
    uint32_t ear_twitch_start_time; // When current ear twitch started  
    bool ear_twitching;             // Currently ear twitching
} sprite_manager_t;

// Function declarations
void sprite_manager_init(sprite_manager_t* manager);
void sprite_manager_update(sprite_manager_t* manager, uint32_t current_time);
void sprite_manager_set_state(sprite_manager_t* manager, animation_state_t new_state, uint32_t current_time);
void sprite_render_layers(sprite_manager_t* manager, lv_obj_t* canvas, uint32_t current_time);

#endif // ANIMATIONS_SPRITES_H 