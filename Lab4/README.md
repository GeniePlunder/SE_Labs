# Frogger Lab

This project is a single-topic road-crossing Frogger game using
**Pygame**. It introduces students to overlap-based collision
detection, a lives/respawn system, win-condition logic, and round
timing, using a small, readable object-oriented codebase.

---

## What's Provided

A working Frogger game with:

- A frog that hops one grid cell at a time with the arrow keys
- Vehicles that scroll across six road lanes at different speeds and
  directions, wrapping around the screen
- A goal zone at the top and a starting zone at the bottom
- Restart support (press R)

It has **one deliberate bug** and **three features** left for you to
build. You are expected to **analyze**, **interact with an AI
assistant**, and **complete/fix** the game to make it fully functional
and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python main.py
```

**Controls:** Arrow keys hop the frog one grid cell at a time (up,
down, left, right). Press R at any time to restart.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM
suggestions and your critical code review.

### Task 1: Fix vehicle collision detection

> **What you'll see:** the frog sometimes drives straight through a
> vehicle that's clearly overlapping it, especially in the faster
> lanes - collisions feel inconsistent rather than reliably fatal.
>
> **Why:** collision detection compares grid columns rather than
> checking whether the frog and a vehicle actually overlap, so
> collisions are sometimes missed, especially with vehicles moving at
> different speeds.
>
> **Fix it:** base the detection on the frog's and vehicles' real
> positions and sizes, not their grid columns. This task is only about
> detecting collisions correctly - don't add lives yet.

### Task 2: Implement lives and respawn

> Add a 3-life system. When the frog collides with a vehicle:
> - decrease the remaining lives by one
> - reset the frog to its starting position
> - let the player continue if lives remain
> - display the number of remaining lives
> - end the game once all lives are used up
>
> The moment of collision should be something the player can actually
> see happen - watch closely what your implementation does the
> instant a hit occurs, not just what the board looks like a moment
> later.

### Task 3: Implement goal and score tracking

> When the frog successfully reaches the goal, the game should end in
> a win:
> - register the successful crossing
> - increase the score
> - end the game with a clear "You Won!" message
>
> Display the current score during gameplay.

### Task 4: Add a 30-second timer

> Add a 30-second countdown for each attempt.
> - Display the remaining time.
> - Start the timer when an attempt begins.
> - If the timer reaches zero before the goal is reached, the attempt
>   should end as a genuine failure - think about how this should
>   interact with the lives system from Task 2, not just reset
>   silently with no consequence.
> - If the frog reaches the goal before time runs out, that's a win
>   (Task 3) regardless of how much time is left.
> - The timer should reset correctly when starting a new game.

---

## Expected Behavior

- Arrow keys hop the frog one grid cell at a time in any direction.
- The frog cannot move below its own starting row.
- A collision is only registered when the frog and a vehicle actually
  visually overlap - not because they merely share a lane.
- The player can see the moment they get hit, not just an instant,
  unexplained teleport back to the start.
- Losing all 3 lives ends the game with a "Game Over" message.
- Reaching the goal ends the game with a "You Won!" message.
- Running out of time on an attempt is treated as a genuine failed
  attempt, not a free reset.
- Pressing R at any time restarts the whole game from scratch.

---

## Folder Structure

```
frogger/
├── main.py
├── requirements.txt
├── game/
│   ├── game_engine.py
│   ├── frog.py
│   ├── vehicle.py
│   ├── collisions.py
│   └── renderer.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [ ] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [ ] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [ ] The Chat/LLM used page link, with the complete chat history
