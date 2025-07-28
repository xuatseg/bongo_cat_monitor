# 🎭 Bongo Cat Animation System Description

## 📋 **LAYER SYSTEM (Z-order from back to front):**
1. **LAYER_BODY** (back) - Standard body or ear twitch body
2. **LAYER_FACE** - Stock, happy, sleepy, or blink face  
3. **LAYER_TABLE** - Always table1 sprite
4. **LAYER_PAWS** - Left/right paw down or both paws up
5. **LAYER_EFFECTS** (front) - Click effects or sleepy effects

---

## 🎯 **ANIMATION STATES DETAILED:**

### **1. ANIM_STATE_IDLE_STAGE1 - "Short Idle"**
**What it does:** Shows cat with both paws up (visible above table)
**Sprites:**
- Body: `standardbody1`
- Face: `stock_face` 
- Table: `table1`
- Paws: `twopawsup` (both paws visible above table)
- Effects: `NULL`

**Rules:**
- Triggered when typing stops
- Paw animation disabled
- Can blink (random 3-8 seconds)
- Can ear twitch (random 10-30 seconds)
- **Auto-progression:** After 3 seconds → IDLE_STAGE2

---

### **2. ANIM_STATE_IDLE_STAGE2 - "Mid Idle"** 
**What it does:** Removes paws (hands go underneath table) but keeps stock face
**Sprites:**
- Body: `standardbody1`
- Face: `stock_face` (still normal face)
- Table: `table1`
- Paws: `NULL` (no paws visible - hands underneath table)
- Effects: `NULL`

**Rules:**
- Can blink (random 3-8 seconds)
- Can ear twitch (random 10-30 seconds)
- **Auto-progression:** After 5 seconds → IDLE_STAGE3

---

### **3. ANIM_STATE_IDLE_STAGE3 - "Deep Sleep Preparation"**
**What it does:** No paws + sleepy face, preparing for deep sleep
**Sprites:**
- Body: `standardbody1`
- Face: `sleepy_face`
- Table: `table1` 
- Paws: `NULL` (no paws visible)
- Effects: `NULL`

**Rules:**
- **NO BLINKING** (cat is too sleepy)
- Can ear twitch (random 10-30 seconds)
- **Auto-progression:** After 7 seconds → IDLE_STAGE4

---

### **4. ANIM_STATE_IDLE_STAGE4 - "Deep Sleep with Effects"**
**What it does:** Deep sleep with cycling sleepy effects (ZZZ animations)
**Sprites:**
- Body: `standardbody1`
- Face: `sleepy_face`
- Table: `table1`
- Paws: `NULL` (no paws visible)
- Effects: Cycles through `sleepy1` → `sleepy2` → `sleepy3` → repeat every 1 second

**Rules:**
- **NO BLINKING** (deep sleep)
- Can ear twitch (random 10-30 seconds)
- Cycling sleepy effects create ZZZ animation loop

---

### **5. ANIM_STATE_TYPING_SLOW - "Slow Typing"**
**What it does:** Basic paw typing pattern with pauses
**Sprites:**
- Body: `standardbody1` 
- Face: `stock_face`
- Table: `table1`
- Paws: **Pattern:** `leftpawdown` → `twopawsup` → `rightpawdown` → `twopawsup` → repeat
- Effects: `NULL` (no click effects)

**Rules:**
- 4-step paw animation cycle with both-paws-up between each strike
- Speed controlled by Python WPM calculation
- Can blink (random 3-8 seconds)
- Can ear twitch (random 10-30 seconds)

---

### **6. ANIM_STATE_TYPING_NORMAL - "Normal Typing"**  
**What it does:** Same 4-step pattern as slow typing but faster
**Sprites:**
- Body: `standardbody1`
- Face: `stock_face`
- Table: `table1` 
- Paws: **Pattern:** `leftpawdown` → `twopawsup` → `rightpawdown` → `twopawsup` → repeat
- Effects: `NULL` (no click effects)

**Rules:**
- Same 4-step pattern as slow typing but with faster animation speed

---

### **7. ANIM_STATE_TYPING_FAST - "Fast Typing with Effects"**
**What it does:** 4-step paw pattern + synchronized click effects
**Sprites:**
- Body: `standardbody1`
- Face: `stock_face`
- Table: `table1`
- Paws: **Pattern:** `leftpawdown` → `twopawsup` → `rightpawdown` → `twopawsup` → repeat
- Effects: `left_click_effect` (with left paw) → `NULL` → `right_click_effect` (with right paw) → `NULL` → repeat

**Rules:**
- 4-step paw animation with click effects synchronized to paw strikes
- Click effects only show during paw-down phases
- Can blink and ear twitch

---

### **8. ANIM_STATE_TYPING_STREAK - "Typing Streak (Happy Face)"**
**What it does:** Same animation as current typing speed but with happy face
**Sprites:**
- Body: `standardbody1`
- Face: `happy_face` ⭐ **ONLY CHANGE - face swap**
- Table: `table1`
- Paws: **Same pattern as current typing state**
- Effects: **Same effects as current typing state**

**Rules:**
- **IMPORTANT:** Streak mode does NOT change speed or effects
- It simply swaps the face to `happy_face` regardless of typing speed
- If streak during slow typing: slow pattern + happy face
- If streak during fast typing: fast pattern + effects + happy face
- Triggered by sustained high WPM (65+ in Python)

---

## 🎲 **AUTOMATIC BEHAVIORS:**

### **Blinking Animation**
- **When:** All states EXCEPT IDLE_STAGE3 and IDLE_STAGE4
- **Pattern:** Swap to `blink_face` for 200ms, then back to normal face
- **Timing:** Random interval 3-8 seconds
- **Face restoration:** Returns to appropriate face based on current state

### **Ear Twitch Animation** 
- **When:** All states (random background animation)
- **Pattern:** Swap to `bodyeartwitch` for 500ms, then back to `standardbody1`
- **Timing:** Random interval 10-30 seconds

---

## 🔄 **STATE TRANSITIONS:**

### **Idle Progression (when typing stops):**
```
TYPING → IDLE_STAGE1 (stock face, paws up, 3s) 
      → IDLE_STAGE2 (stock face, paws down, 5s) 
      → IDLE_STAGE3 (sleepy face, paws down, no blinking, 7s) 
      → IDLE_STAGE4 (sleepy face, paws down, sleep effects, no blinking)
```

### **Typing Activation (when typing starts):**
```
Any IDLE_STATE → Appropriate TYPING_STATE (based on WPM)
```

### **Streak Activation:**
```
Any TYPING_STATE → Same TYPING_STATE but with happy_face
``` 