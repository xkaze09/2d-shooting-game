from ursina import *

app = Ursina()
window.fullscreen = False
player = Entity(model='quad', texture='assets\player',
                collider='box', y=5, scale=2)
bg = Entity(model='quad', texture='assets\BG', scale=36, z=1)
target = Entity(model='cube', texture='assets\\target1',
                collider='box', scale=2, x=20, y=-10)


targets = []


def newTarget():
    new = duplicate(target, y=-5+(5124*time.dt) % 15)
    targets.append(new)
    invoke(newTarget, delay=1)


newTarget()
camera.orthographic = True
camera.fov = 20


def update():
    global score, text
    player.y += held_keys['w'] * 6 * time.dt
    player.y -= held_keys['s'] * 6 * time.dt
    player.x += held_keys['d'] * 6 * time.dt
    player.x -= held_keys['a'] * 6 * time.dt
    a = held_keys['w'] * -20
    b = held_keys['s'] * 20
    if a != 0:
        player.rotation_z = a
    else:
        player.rotation_z = b
    for target in targets:
        target.x -= 4*time.dt
        touch = target.intersects()
        if touch.hit:
            targets.remove(target)
            destroy(target)
            destroy(touch.entity)
            score += 1
            text.y = 10
            text = Text(text=f"Score: {score}", position=(-.65, .4),
                        origin=(0, 0), scale=2, color=color.yellow, background=True)
    t = player.intersects()
    if t.hit and t.entity.scale == 2:
        quit()


def input(key):
    if key == 'space':
        e = Entity(y=player.y, x=player.x+1, model='cube', scale=1,
                   texture='assets\Bullet', collider='cube')
        e.animate_x(30, duration=2, curve=curve.linear)
        invoke(destroy, e, delay=2)


score = 0
text = Text(text='')
text = Text(text=f"Score: {score}", position=(-.65, .4),
            origin=(0, 0), scale=2, color=color.yellow, background=True)


app.run()
