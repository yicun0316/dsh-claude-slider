import re
import os

def update_demo_html(fp):
    if not os.path.exists(fp):
        print(f"File not found: {fp}")
        return
    with open(fp, "r", encoding="utf-8") as f:
        code = f.read()

    # 1. 确保 DEFAULT_CONFIG 中有 soundVolume: 1.0
    if 'soundType: "zako",' in code and 'soundVolume: 1.0' not in code:
        code = code.replace(
            'soundType: "zako",',
            'soundType: "zako",\n      soundVolume: 1.0,'
        )
        print(f"[{os.path.basename(fp)}] Added soundVolume: 1.0 to DEFAULT_CONFIG")

    # 2. 插入 getSoundVolume 辅助函数
    get_sound_vol_func = """    function getSoundVolume() {
      if (typeof globalConfig !== "undefined" && globalConfig && globalConfig.soundEnabled === false) return 0;
      if (typeof soundEnabled !== "undefined" && !soundEnabled) return 0;
      const vol = typeof globalConfig !== "undefined" && typeof globalConfig.soundVolume === "number" 
        ? globalConfig.soundVolume 
        : (typeof soundVolume !== "undefined" ? soundVolume : 1.0);
      return Math.max(0, Math.min(2.0, vol));
    }
"""
    if "function getSoundVolume()" not in code:
        code = code.replace(
            "function playAudioBuffer(ctx, buffer, gainVal = 0.55) {",
            get_sound_vol_func + "\n    function playAudioBuffer(ctx, buffer, gainVal = 0.55) {"
        )
        print(f"[{os.path.basename(fp)}] Added getSoundVolume() function")

    # 3. 更新所有 playAudioBuffer 里的 gainVal 为 gainVal * masterVol
    old_play_buf = """        gainNode.gain.setValueAtTime(gainVal, ctx.currentTime);"""
    new_play_buf = """        const masterVol = getSoundVolume();
        if (masterVol <= 0.001) return true;
        gainNode.gain.setValueAtTime(gainVal * masterVol, ctx.currentTime);"""
    
    if old_play_buf in code:
        code = code.replace(old_play_buf, new_play_buf)
        print(f"[{os.path.basename(fp)}] Updated playAudioBuffer with masterVol")

    # 4. 更新 playMechanicalTick
    old_mech = """        gain.gain.setValueAtTime(0.08, now);
        gain.gain.exponentialRampToValueAtTime(0.001, now + 0.035);"""
    new_mech = """        const masterVol = getSoundVolume();
        if (masterVol <= 0.001) return;
        gain.gain.setValueAtTime(0.08 * masterVol, now);
        gain.gain.exponentialRampToValueAtTime(0.001 * masterVol, now + 0.035);"""
    
    if old_mech in code:
        code = code.replace(old_mech, new_mech)
        print(f"[{os.path.basename(fp)}] Updated playMechanicalTick with masterVol")

    # 5. 更新 playDuckSqueak
    old_duck = """        gain1.gain.setValueAtTime(0.001, now);
        gain1.gain.linearRampToValueAtTime(0.28, now + 0.03);
        gain1.gain.exponentialRampToValueAtTime(0.001, now + 0.11);

        osc1.connect(filter);
        filter.connect(gain1);
        gain1.connect(ctx.destination);
        osc1.start(now);
        osc1.stop(now + 0.11);

        const osc2 = ctx.createOscillator();
        const gain2 = ctx.createGain();
        osc2.type = "sine";
        osc2.frequency.setValueAtTime(2000, now + 0.13);
        osc2.frequency.exponentialRampToValueAtTime(2600, now + 0.16);
        osc2.frequency.exponentialRampToValueAtTime(1800, now + 0.20);

        gain2.gain.setValueAtTime(0.001, now + 0.13);
        gain2.gain.linearRampToValueAtTime(0.18, now + 0.15);
        gain2.gain.exponentialRampToValueAtTime(0.001, now + 0.20);"""

    new_duck = """        const masterVol = getSoundVolume();
        if (masterVol <= 0.001) return;
        gain1.gain.setValueAtTime(0.001, now);
        gain1.gain.linearRampToValueAtTime(0.28 * masterVol, now + 0.03);
        gain1.gain.exponentialRampToValueAtTime(0.001 * masterVol, now + 0.11);

        osc1.connect(filter);
        filter.connect(gain1);
        gain1.connect(ctx.destination);
        osc1.start(now);
        osc1.stop(now + 0.11);

        const osc2 = ctx.createOscillator();
        const gain2 = ctx.createGain();
        osc2.type = "sine";
        osc2.frequency.setValueAtTime(2000, now + 0.13);
        osc2.frequency.exponentialRampToValueAtTime(2600, now + 0.16);
        osc2.frequency.exponentialRampToValueAtTime(1800, now + 0.20);

        gain2.gain.setValueAtTime(0.001, now + 0.13);
        gain2.gain.linearRampToValueAtTime(0.18 * masterVol, now + 0.15);
        gain2.gain.exponentialRampToValueAtTime(0.001 * masterVol, now + 0.20);"""

    if old_duck in code:
        code = code.replace(old_duck, new_duck)
        print(f"[{os.path.basename(fp)}] Updated playDuckSqueak with masterVol")

    # 6. 更新 playDialTick 支持 forcePlay
    old_dial = """    function playDialTick() {
      if (globalConfig.soundEnabled === false) return;"""
    new_dial = """    function playDialTick(forcePlay = false) {
      if (globalConfig.soundEnabled === false && !forcePlay) return;
      const vol = typeof globalConfig.soundVolume === "number" ? globalConfig.soundVolume : 1.0;
      if (vol <= 0.001 && !forcePlay) return;"""
    if old_dial in code:
        code = code.replace(old_dial, new_dial)
        print(f"[{os.path.basename(fp)}] Updated playDialTick in React section")

    # 7. 在 QuickDrawer (TAB 3: tuning) 中添加音量调节滑块
    volume_slider_quickdrawer = """              // 🔊 音量大小调节滑块
              config.soundEnabled !== false && h("div", { className: "dcs-tuning-group", style: { marginTop: 8 } },
                h("div", { className: "dcs-tuning-header" },
                  h("span", { className: "dcs-tuning-label" }, "🔊 吸附音量 (Volume)"),
                  h("span", { className: "dcs-tuning-val", style: { color: config.accentColor || "#4D6BFE" } },
                    (config.soundVolume === 0) ? "0% (静音)" : `${Math.round((config.soundVolume !== undefined ? config.soundVolume : 1.0) * 100)}%`
                  )
                ),
                h("div", { className: "dcs-tuning-slider-row" },
                  h("input", {
                    type: "range",
                    min: 0,
                    max: 1.5,
                    step: 0.05,
                    value: config.soundVolume !== undefined ? config.soundVolume : 1.0,
                    className: "dcs-range-input",
                    onChange: (e) => {
                      const val = parseFloat(e.target.value);
                      configStore.update({ soundVolume: val });
                    },
                    onMouseUp: () => playDialTick(true),
                    onTouchEnd: () => playDialTick(true)
                  }),
                  h("button", {
                    type: "button",
                    className: "dcs-tuning-reset-btn",
                    title: "试听当前音量",
                    style: { marginRight: 4 },
                    onClick: () => playDialTick(true)
                  }, "试听"),
                  h("button", {
                    type: "button",
                    className: "dcs-tuning-reset-btn",
                    title: "恢复默认 100% 音量",
                    onClick: () => {
                      configStore.update({ soundVolume: 1.0 });
                      setTimeout(() => playDialTick(true), 20);
                    }
                  }, "复位")
                )
              ),
"""
    target_drawer_input = """              h("input", {
                ref: soundFileInputRef,
                type: "file",
                accept: "audio/*",
                style: { display: "none" },
                onChange: handleSoundUpload
              })
            )
          ),

          h("div", { className: "dcs-tuning-group", style: { marginTop: 6 } },"""

    if "🔊 吸附音量 (Volume)" not in code and target_drawer_input in code:
        code = code.replace(
            target_drawer_input,
            """              h("input", {
                ref: soundFileInputRef,
                type: "file",
                accept: "audio/*",
                style: { display: "none" },
                onChange: handleSoundUpload
              }),
""" + volume_slider_quickdrawer + """            )
          ),

          h("div", { className: "dcs-tuning-group", style: { marginTop: 6 } },"""
        )
        print(f"[{os.path.basename(fp)}] Added volume slider to QuickDrawer TAB 3 in demo")

    # 8. 在 ClaudeSettingsPage 中添加音量调节滑块
    target_settings_input = """              h("input", {
                ref: soundFileInputRef,
                type: "file",
                accept: "audio/*",
                style: { display: "none" },
                onChange: handleSoundUpload
              })
            )
          ),

          // 1. 动效模式（29 大四字纯净动效网格）"""

    volume_slider_settings = """              // 🔊 音量大小调节滑块
              config.soundEnabled !== false && h("div", { className: "dcs-tuning-group", style: { marginTop: 10, width: "100%" } },
                h("div", { className: "dcs-tuning-header" },
                  h("span", { className: "dcs-tuning-label" }, "🔊 吸附音量大小 (Volume)"),
                  h("span", { className: "dcs-tuning-val", style: { color: config.accentColor || "#4D6BFE" } },
                    (config.soundVolume === 0) ? "0% (静音)" : `${Math.round((config.soundVolume !== undefined ? config.soundVolume : 1.0) * 100)}%`
                  )
                ),
                h("div", { className: "dcs-tuning-slider-row" },
                  h("input", {
                    type: "range",
                    min: 0,
                    max: 1.5,
                    step: 0.05,
                    value: config.soundVolume !== undefined ? config.soundVolume : 1.0,
                    className: "dcs-range-input",
                    onChange: (e) => {
                      const val = parseFloat(e.target.value);
                      configStore.update({ soundVolume: val });
                    },
                    onMouseUp: () => playDialTick(true),
                    onTouchEnd: () => playDialTick(true)
                  }),
                  h("button", {
                    type: "button",
                    className: "dcs-tuning-reset-btn",
                    title: "试听当前音量",
                    style: { marginRight: 6 },
                    onClick: () => playDialTick(true)
                  }, "试听"),
                  h("button", {
                    type: "button",
                    className: "dcs-tuning-reset-btn",
                    title: "恢复默认 100% 音量",
                    onClick: () => {
                      configStore.update({ soundVolume: 1.0 });
                      setTimeout(() => playDialTick(true), 20);
                    }
                  }, "复位为 100%")
                )
              ),
"""

    if "🔊 吸附音量大小 (Volume)" not in code and target_settings_input in code:
        code = code.replace(
            target_settings_input,
            """              h("input", {
                ref: soundFileInputRef,
                type: "file",
                accept: "audio/*",
                style: { display: "none" },
                onChange: handleSoundUpload
              }),
""" + volume_slider_settings + """            )
          ),

          // 1. 动效模式（29 大四字纯净动效网格）"""
        )
        print(f"[{os.path.basename(fp)}] Added volume slider to ClaudeSettingsPage in demo")

    with open(fp, "w", encoding="utf-8") as f:
        f.write(code)
    print(f"[{os.path.basename(fp)}] Successfully saved demo/index.html updates!")

update_demo_html(r"C:\Users\王文岩\.dsh\profiles\desktop\node_modules\dsh-claude-slider\demo\index.html")
update_demo_html(r"C:\Users\王文岩\.gemini\antigravity\scratch\dsh-claude-slider\demo\index.html")
