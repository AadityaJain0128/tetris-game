# Quick Start Guide - Tetris Ultimate Edition

## 🚀 Get Started in 3 Steps

### 1. Install
```bash
git clone https://github.com/yourusername/tetris-ultimate.git
cd tetris-ultimate
pip install -r requirements.txt
```

### 2. Run
```bash
python tetris.py
```

### 3. Play!
- **←/→** - Move left/right
- **↓** - Soft drop
- **↑** - Rotate
- **SPACE** - Hard drop
- **C** - Hold piece
- **G** - Toggle ghost

## 🎯 Quick Tips

### Scoring
- **Single** (1 line): 100 × level
- **Double** (2 lines): 300 × level  
- **Triple** (3 lines): 500 × level
- **Tetris** (4 lines): 800 × level

### Strategy
1. **Use Ghost Piece** - See where your piece will land
2. **Hold Feature** - Save pieces for better opportunities
3. **Build Flat** - Avoid creating gaps
4. **Plan Ahead** - Check the next piece preview

### Controls Reference
| Key | Action |
|-----|--------|
| ← → | Move horizontally |
| ↓ | Move down faster (+1 point/row) |
| ↑ | Rotate piece |
| SPACE | Drop instantly (+2 points/row) |
| C | Swap with hold piece |
| G | Show/hide ghost piece |
| R | Restart (when game over) |
| ESC | Quit game |

## 🔧 Troubleshooting

### Game won't start?
```bash
# Make sure pygame is installed
pip install pygame

# Try reinstalling
pip uninstall pygame
pip install pygame
```

### Import errors?
```bash
# Make sure you're in the right directory
cd tetris-ultimate

# Check Python version (need 3.8+)
python --version
```

### Performance issues?
- Close other applications
- Update graphics drivers
- Try reducing window size (edit BLOCK_SIZE in tetris.py)

## 📦 Package Installation

### Install as a package:
```bash
pip install -e .
tetris  # Run from anywhere!
```

### Create executable:
```bash
pip install pyinstaller
pyinstaller --onefile --windowed --name TetrisUltimate tetris.py
# Executable will be in dist/ folder
```

## 🎮 Gameplay Features

✅ Classic Tetris with all 7 pieces  
✅ Ghost piece preview  
✅ Hold piece functionality  
✅ Next piece preview  
✅ Animated line clearing  
✅ Progressive difficulty  
✅ Advanced scoring system  

## 🆘 Need Help?

- 📖 Read the [full README](README.md)
- 🐛 [Report bugs](https://github.com/yourusername/tetris-ultimate/issues)
- 💬 [Ask questions](https://github.com/yourusername/tetris-ultimate/discussions)

## 🎊 Have Fun!

Enjoy playing Tetris Ultimate Edition! Try to beat your high score and reach the highest level possible!

---

**Made with ❤️ using Python and Pygame**
