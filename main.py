#Consegui as imagens e áudios por meio do site Opengameart
#Em questão de pygame, tive que usar a documentação contida no site do pygame para poder usar algumas funcionalidades como música, sprites, colisões e etc.
#Para melhorar meu código utilizei inúmeros sites e fóruns tais como Reddit, StackOverflow e Github
#Caso possua alguma dúvida sobre meu projeto pode me contactar

#Diferenca

#importe de bibliotecas usadas no código:
import random
import sys
import pygame
import pygame.constants
import pygame.sprite

#variáveis globais

threat = False
final_enemyDead = False
last_drones = False
bike_dead = False
drones_dead = False
can_shoot = False
first_droneDown = False
delay_shoot = False
boss_music = True
first_enemyDead = False
second_enemyDead = False
clock_tick_rate = 25   #FPS do jogo
Comprimento_Tela = 2512
Altura_Tela = 304
velocidade = 10
ALPHA = (0, 0, 0)    #definição da cor preta
win = pygame.display.set_mode((Comprimento_Tela, Altura_Tela))  #define o tamanho da tela e seu comprimento
true_scroll = [0, 0]
level = 0

#criação dos grupos de sprites
barravida = pygame.sprite.Group()
invisible_enemies = pygame.sprite.Group()
vehicles = pygame.sprite.Group()
Bosses = pygame.sprite.Group()
pocoes = pygame.sprite.Group()
spells = pygame.sprite.Group()
background_list = pygame.sprite.Group()
jogadores = pygame.sprite.Group()
grounds = pygame.sprite.Group()
all_spriteslevel0 = pygame.sprite.Group()
bullets = pygame.sprite.Group()
platforms = pygame.sprite.Group()
boss_spells = pygame.sprite.Group()
all_spriteslevel1 = pygame.sprite.Group()


def toca_musica(caminho):
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.play()

def musica_fundo(caminho):
    pygame.mixer.music.load(caminho)
    pygame.mixer.music.play(-1)
    pygame.mixer.music.set_volume(0.2)

#função que eu usei para carregar as imagens, virar elas horizontalmente quando necessário e se elas estiverem com um fundo preto torná-lo transparente
def carregar_sprite(caminho,flip=False):
    imagem = pygame.image.load(caminho).convert()
    if flip:
        imagem = pygame.transform.flip((imagem), True, False)
    imagem.convert_alpha()
    imagem.set_colorkey(ALPHA)
    return imagem


#Lista com as imagens da barra de vida, desde ela completa até ela vazia
health_ani = [
    carregar_sprite("Data/Helath_0_pecent.png"),
    carregar_sprite("Data/Helath_10_pecent.png"),
    carregar_sprite("Data/Helath_20_pecent.png"),
    carregar_sprite("Data/Helath_30_pecent.png"),
    carregar_sprite("Data/Helath_40_pecent.png"),
    carregar_sprite("Data/Helath_50_pecent.png"),
    carregar_sprite("Data/Helath_60_pecent.png"),
    carregar_sprite("Data/Helath_70_pecent.png"),
    carregar_sprite("Data/Helath_80_pecent.png"),
    carregar_sprite("Data/Helath_90_pecent.png"),
    carregar_sprite("Data/Helath_100_pecent.png"),
]
#dicionário com as imagens das plataformas utilizadas
Plataformas = {
    "groundFase2":carregar_sprite("Data/GroundFase2.png"),
    "plat_landing":carregar_sprite("Data/plataformalanding.png"),
    "plat_long":carregar_sprite("Data/plataforma2.png"),
    "plat_cave":carregar_sprite("Data/plataforma3.png")
}

#dicionário usado para guardar as imagens e seus loads, pois se tivesse feito os loads durante o código poderia afetar o desempenho do jogo.
Imagens = {
    "BolaAgua":carregar_sprite("Data/WaterBall.png"),
    "Tornado":carregar_sprite("Data/WaterTornado.png"),
    "ImagemFinal":carregar_sprite("Data/ImagemFinal.png"),
    "RocketEsquerda":carregar_sprite("Data/Rocket.png"),
    "RocketDireita":carregar_sprite("Data/Rocket.png",flip=True),
    "TurretBullet":carregar_sprite("Data/turretbullet.png"),
    "RaioDireita":carregar_sprite("Data/Lightning.png"),
    "RaioEsquerda":carregar_sprite("Data/Lightning.png",flip=True),
    "Turret":carregar_sprite("Data/FinalTurret.png"),
    "Biker":carregar_sprite("Data/BikeRider.png"),
    "LaserDireita":carregar_sprite("Data/laser.png"),
    "LaserEsquerda":carregar_sprite("Data/laser.png",flip=True),
    "DroneEsquerda":carregar_sprite("Data/Drone.png"),
    "DroneDireita":carregar_sprite("Data/Drone.png",flip=True),
    "EntreFases":carregar_sprite("Data/BetweenScreens.png"),
    "SegundaFase":carregar_sprite("Data/TelaFase2.png"),
    "FimdeJogo":carregar_sprite("Data/GameOver.png"),
    "TelaInicio":carregar_sprite("Data/TelaInicio.png"),
    "bala_direita":carregar_sprite("Data/fireball.png"),
    "bala_esquerda":carregar_sprite("Data/fireball.png", flip=True),
    "Jogador_direita": carregar_sprite("Data/necromante.png"),
    "Jogador_esquerda":carregar_sprite("Data/necromante.png", flip=True),
    "Cenário":carregar_sprite("Data/Tentativa11.png"),
    "Mage_Direita":carregar_sprite("Data/DarkMage.png"),
    "Mage_Esquerda":carregar_sprite("Data/DarkMage.png", flip=True),
    "spell_direita":carregar_sprite("Data/spell_npc.png"),
    "spell_esquerda":carregar_sprite("Data/spell_npc.png",flip=True),
    "PocaoDeVida":carregar_sprite("Data/PocaoVida.png"),
    "ImpVoador_Esquerda":carregar_sprite("Data/ImpVoador.png",flip=True),
    "ImpVoador_Direita":carregar_sprite("Data/ImpVoador.png"),
    "BossLevel1":carregar_sprite("Data/BossLevel1.png",flip=True),

}
#classe da bola de água que o boss lança na primeira fase, a instrução rect cria um retângulo a partir da imagem que carreguei como imagem da sprite.
class WaterBall(pygame.sprite.Sprite):
    def __init__(self, x , y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Imagens["BolaAgua"]
        self.rect = self.image.get_rect()
        self.rect.centerx = x - 20
        self.rect.top = y + 20
        self.health = 1
        self.speedx = 10

#criei um vetor que calcula a distancia do jogador a bola de água, normaliza ela e move em direção ao jogador. Temos também a colisão do tornado com balas, em que caso seja atingido é morto.
    def update(self):
        if level == 0:
            if boss1.health ==0:
                self.kill()
            if self.health != 0:
                dirvect = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
                dirvect.normalize()
                dirvect.scale_to_length(self.speedx)
                self.rect.move_ip(dirvect)
            hit = pygame.sprite.spritecollide(self, bullets, True)
            if hit:
                if self.health > 0:
                    print(self.health)
                    self.health -= 1
                if self.health <= 0:
                    self.kill()


#classe do tornado de água
class WaterTornado(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Imagens["Tornado"]
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(1300, 2100)     #isso faz com que as coordenadas iniciais sejam aleatórias
        self.rect. y = random.randint(0, 200)
        self.health = 1
        self.speedx = 5

#Aqui temos o mesmo esquema feito para a bola de água, em que criamos um vetor para calcular a distancia em relação ao jogador e se mover em direção a ele.
    def update(self):
        if level == 0:
            if boss1.health == 0:
                self.kill()
            if self.health != 0:
                dirvect = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
                dirvect.normalize()
                dirvect.scale_to_length(self.speedx)
                self.rect.move_ip(dirvect)
            hit = pygame.sprite.spritecollide(self, bullets, True)
            if hit:
                if self.health > 0:
                    print(self.health)
                    self.health -= 1
                if self.health <= 0:
                    self.kill()



#classe do foguete lançado pela torreta da segunda fase
class Rocket(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Imagens["RocketEsquerda"]
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 20
        self.rect.centerx = x - 30
        self.speedx = + 15
        self.health = 1


#Código que faz o foguete seguir o player depois de sair da torreta, caso atinja com o feitiço do jogador ele é eliminado e emite um som.
    def update(self):
        if self.health != 0:
            dirvect = pygame.math.Vector2(player.rect.x - self.rect.x, player.rect.y - self.rect.y)
            dirvect.normalize()
            dirvect.scale_to_length(self.speedx)
            self.rect.move_ip(dirvect)
#Caso a coordenada do jogador seja maior que a do foguete a imagem é direita e caso seja menor a imagem é esquerda
        if player.rect.x > self.rect.x:
            self.image = Imagens["RocketDireita"]
        if player.rect.x < self.rect.x:
            self.image = Imagens["RocketEsquerda"]

        hit = pygame.sprite.spritecollide(self, bullets, True)
        if hit:
            if self.health > 0:
                print(self.health)
                self.health -= 1
                pygame.mixer.Channel(14).play(pygame.mixer.Sound("Data/8bit_bomb_explosion.wav"))
            if self.health <= 0:
                self.kill()



#classe que caracteriza as balas que a torreta lança
class TurretBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = Imagens["TurretBullet"]
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 20
        self.rect.centerx = x - 30
        self.speedx = + 10

#faz com que a bala mova-se com essa velocidade no eixo X
    def update(self):
        self.rect.x -= self.speedx

#classe da torreta final da segunda fase
class FinalTurret(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Imagens["Turret"]
        self.rect = self.image.get_rect()
        self.rect.x = 2200
        self.rect.y = 234
        self.health = 8

#temos o código que faz atirar o foguete. Se a vida da torreta é maior que 0 adicionamos uma variável a classe do foguete e adicionamos ela a um grupo de sprites e feitiços.
    def fire(self):
        if self.health > 0:
            rocket = Rocket(self.rect.centerx, self.rect.top)
            all_spriteslevel1.add(rocket)
            spells.add(rocket)

#Caso a vida da torreta seja maior que 0 ela vai dar dois tiros na mesma direção, adicionando duas variáveis nos grupos de sprites do level 1 e no grupo de feitiços.
    def shoot(self):
        if self.health >0:
            tiro = TurretBullet(self.rect.centerx, self.rect.top)
            all_spriteslevel1.add(tiro)
            spells.add(tiro)
            tiro1 = TurretBullet(self.rect.centerx, self.rect.top - 5)
            all_spriteslevel1.add(tiro1)
            spells.add(tiro1)

#Aqui temos o código da colisão da torreta com as balas do jogador, se colidir a bala do jogador sai da tela e a torreta perde vida, gerando um som. Se a vida for menor que zero a torreta morre e uma variável que o último inimigo foi morto.
    def update(self):
        global final_enemyDead
        if self. health != 0:
            hits = pygame.sprite.spritecollide(self, bullets, True)
            if hits:
                if self.health > 0:
                    print(self.health)
                    self.health -= 1
                    pygame.mixer.Channel(11).play(pygame.mixer.Sound("Data/turret.wav"))
                if self.health <= 0:
                    self.kill()
                    final_enemyDead = True

#classe do motociclista da fase 1
class Biker(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Imagens["Biker"]
        self.rect = self.image.get_rect()
        self.speed = 20
        self.rect.x = 1800
        self.rect.y = 195

#Caso os drones forem mortos o motociclista vai da coordenada inicial dele até o fim da tela, se chegar ao fim da tela ele é retirado.
    def movetowards(self):
        global drones_dead
        global bike_dead
        if drones_dead:
            pygame.mixer.Channel(9).play(pygame.mixer.Sound("Data/bicycle-horn-1.wav"))
            self.rect.x -= self.speed
            if self.rect.x <= 0:
                self.kill()
                pygame.mixer.Channel(9).stop()
                bike_dead = True
            drones_dead = False

#classe do drone para o level 1
class Drone(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Imagens["DroneEsquerda"]
        self.rect = self.image.get_rect()
        self.speed = 3
        self.health = 2
        self.lado = -1

#função que faz com que o drone se mova na direção do jogador, dependendo se as coordenadas do jogador são maiores ou menores o drone muda de lado e seu tiro também
    def movetowards(self, target):
        if self.health != 0:
            dirvect = pygame.math.Vector2(target.rect.x - self.rect.x, target.rect.y - self.rect.y)
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
            self.rect.move_ip(dirvect)
        if target.rect.x > self.rect.x:
            self.lado = 1
            self.image = Imagens["DroneDireita"]
        if target.rect.x < self.rect.x:
            self.lado = -1
            self.image = Imagens["DroneEsquerda"]

#função que caso a vida do drone seja maior que zero ele vai atirar, para isso uma variével recebe a classe e é adicionada a um grupo de sprites do level 1 e ao grupo de feitiços.
    def shoot(self):
        if self.health > 0:
            laser = Lasershoot(self.rect.centerx, self.rect.top, self.lado)
            all_spriteslevel1.add(laser)
            spells.add(laser)

#caso a vida do drone seja maior que 0 ele pode colidir com as balas do jogador e caso colida vai perder 1 de vida e gerar um som. Se a vida for menor que 0 ele morre.
    def update(self):
        if self. health != 0:
            hits = pygame.sprite.spritecollide(self, bullets, True)
            if hits:
                if self.health > 0:
                    print(self.health)
                    self.health -= 1
                    pygame.mixer.Channel(8).play(pygame.mixer.Sound("Data/turret.wav"))
                if self.health <= 0:
                    self.kill()

#classe da barra de vida
class HealthBar(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = health_ani[player.health]
        self.rect = self.image.get_rect()

#Aqui configurei para que ela fique em uma posição acima do jogador e a imagem dela é uma lista criada anteriormente, em que o número da posição da lista corresponde a vida do jogador, se a vida do jogador é 10 ele vai pegar o décimo elemento da lista que é a imagem da barra de vida com 100%
    def update(self):
        self.rect.x = player.rect.x - 25
        self.rect.y = player.rect.y - 15
        self.image = health_ani[player.health]
        if self.image == health_ani[0]:
            self.kill()

#Caso a barra de vida choque com os limites do jogo ela vai ficar no campo visível da tela
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > Comprimento_Tela:
            self.rect.right = Comprimento_Tela
        if self.rect.top < 0:
            self.rect.top = 0

#classe do segundo inimigo da primeira fase
class ImpHell(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Imagens["ImpVoador_Esquerda"]
        self.rect = self.image.get_rect()
        self.rect.x = 1578
        self.rect.y = 90
        self.speed = 9
        self.health = 8

#Caso ele colida com as balas do jogador perde 1 de vida e um som é gerado a partir disso. Se a vida for zerada ele sai da tela e uma variável mostrando que ele morreu é setada.
    def update(self):
        if level == 1:
            self.kill()
        global second_enemyDead
        hit_bullet_imp = pygame.sprite.spritecollide(self, bullets, True)
        if hit_bullet_imp:
            if self.health > 0:
                print(self.health)
                self.health -= 1
                pygame.mixer.Channel(0).play(pygame.mixer.Sound("Data/zombie-7.WAV"))
            if self.health <= 0 or level == 1:
                self.kill()
                second_enemyDead = True

#Função que faz ele seguir o jogador a partir do momento que matamos o primeiro inimigo e dependendo da posição do alvo ele troca a imagem.
    def move_towards_player(self, target):
        if first_enemyDead and player.health > 0:
            dirvect = pygame.math.Vector2(target.rect.x - self.rect.x, target.rect.y - self.rect.y)
            dirvect.normalize()
            dirvect.scale_to_length(self.speed)
            self.rect.move_ip(dirvect)
            if target.rect.x > self.rect.x:
                self.image = Imagens["ImpVoador_Direita"]
            if target.rect.x < self.rect.x:
                self.image = Imagens["ImpVoador_Esquerda"]




#classe da poção de vida onde carregamos a imagem e setamos as coordenadas
class HealthPotion(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Imagens["PocaoDeVida"]
        self.rect = self.image.get_rect()
        self.rect.x = 1028
        self.rect.y = 135


#classe do tiro do drone, em que recebe as coordenadas do drone e é atirado a partir disso, dependendo do lado a imagem do laser é trocada.
class Lasershoot(pygame.sprite.Sprite):
    def __init__(self, x, y, lado):
        pygame.sprite.Sprite.__init__(self)
        if lado == 1:
            self.image = Imagens["LaserDireita"]
        else:
            self.image = Imagens["LaserEsquerda"]
        self.rect = self.image.get_rect()
        self.rect.bottom = y + 35
        self.rect.centerx = x - 20
        self.speedx = - 15
        self.lado = lado

#função da posição variando dependendo da velocidade e do lado que ele está
    def update(self):
        self.rect.x -= self.speedx * self.lado

#classe da magia que o primeiro inimigo da primeira fase lança, dependendo do lado que ele se encontra a imagem dela se altera. Também recebe as coordenadas do inimigo que lança ela para sair de uma certa posição
class Spell(pygame.sprite.Sprite):
    def __init__(self, x, y, lado):
        pygame.sprite.Sprite.__init__(self)
        if lado == 1:
            self.image = Imagens["spell_direita"]
        else:
            self.image = Imagens["spell_esquerda"]

        self.rect = self.image.get_rect()
        self.rect.bottom = y + 35
        self.rect.centerx = x - 20
        self.speedx = -10
        self.lado = lado

#Caso a vida do inmigo seja 0 ela não também vai deixar de existir. A posição a partir de atirada depende da velocidade e do lado. Caso atinja o limite da tela é eliminada.
    def update(self):
        if blackmage.health <=0:
            self.kill()
        self.rect.x -= self.speedx * self.lado
        if self.rect.bottom < 0:
            self.kill()

#classe que pega a imagem do plano de fundo e seu retângulo
class BackGround(pygame.sprite.Sprite):
    def __init__(self, surface):
        pygame.sprite.Sprite.__init__(self)
        self.image = surface
        self.rect = self.image.get_rect()



#classe do primeiro inimigo da primeira fase e seus atributos.
class BlackMage(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Imagens["Mage_Esquerda"]
        self.rect = self.image.get_rect()
        self.rect.x = 700
        self.rect.y = 90
        self.speedyx = 2
        self.health = 7
        self.lado = -1


#Função que faz a colisão dele com as balas do jogador, perdendo 1 de vida se ocorre a colisão e gerando um som. Estava tendo um problema que a imagem dele continuava e o jogador continuava tomando dano então se ele morre jogo ele para um lugar na tela onde não tem como ocorrer colisão.
    def update(self):
        global first_enemyDead
        if level == 1:
            self.kill()
        hit_blackmage_bullet = pygame.sprite.spritecollide(self, bullets, True)
        if hit_blackmage_bullet:
            if self.health > 0:
                print(self.health)
                self.health -= 1
                pygame.mixer.Channel(1).play(pygame.mixer.Sound("Data/deathr.WAV"))
            if self.health <= 0:
                self.rect.x = 200
                self.rect.y = 600
                first_enemyDead = True
                self.kill()



#função que faz esse primeiro inimigo atirar, adicionando o tiro às classes e gerando um som
    def shoot(self):
        if self.health != 0:
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("Data/sfx_step_water_l.FLAC"))
        spell = Spell(self.rect.centerx, self.rect.top, self.lado)
        all_spriteslevel0.add(spell)
        spells.add(spell)

#caso a posição do player seja maior que a do inimigo ele irá virar de lado, caso não permanece igual.
    def virar(self, target):
        if target.rect.x >= 750:
            self.lado = 1
            self.image = Imagens["Mage_Direita"]
        else:
            self.lado = -1
            self.image = Imagens["Mage_Esquerda"]


#classe para o chão da segunda fase que recebe coordenadas da sua localização e imagem
class Ground(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = Plataformas[img]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#classe para as platafromas da primeira fase que recebe coordenadas das suas respectivas localizações. Suas imagens são retiradas de um dicionário feito para armazenar as imagens de plataformas.
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = Plataformas[img]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

#caso o nível avance elas somem
    def update(self):
        if level == 1:
            self.kill()




#classe da magia que o jogador lança, caso o level mude a imagem de fogo altera para imagem de um raio. Suas coordenadas dependem das coordenadas do jogador e para que lado ele está virado.
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, lado,level):
        pygame.sprite.Sprite.__init__(self)
        if lado == 1:
            self.image = Imagens["bala_direita"]
            if level == 1:
                self.image = Imagens["RaioDireita"]
        else:
            self.image = Imagens["bala_esquerda"]
            if level == 1:
                self.image = Imagens["RaioEsquerda"]



        self.rect = self.image.get_rect()
        self.rect.bottom = y + 45
        self.rect.centerx = x + 30*(lado)
        self.speedy = -20
        self.lado = lado
        self. level = level
        self.viajou = 0

#criei uma variável viajou para destruir a bala a partir de uma certa distancia que ele percorre. Para a atualização da localização dela levamos em conta sua velocidade e lado. Se atingir o limite da tela ela é eliminada.
    def update(self) :
        self.viajou += self.rect.centerx/self.rect.centerx
        if self.viajou >= 43:
            self.kill()
        if pygame.sprite.collide_rect(player, blackmage):
            self.kill()

        self.rect.x -= self.speedy * self.lado
        if self.rect.bottom < 0:
            self.kill()



#classe feita para o jogador. Jogador sempre começa do lado direito então lado é 1. Começa caindo então a variável falling é True.
class Player(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Imagens["Jogador_direita"]
        self.rect = self.image.get_rect()
        self.lado = 1
        self.health = 10
        self.isJumping = False
        self.visible = True
        self.isFalling = True
        self.aceleracao = 3
        self.velocidade = 0
        self.left = False
        self.right = True
        self.restored = False

#função que restaura a vida do jogador quando alcança o level 1.
    def life(self):
        if level == 1 and not self.restored:
            self.restored = True
            self.health = 10

#Definição da gravidade para o jogador. Caso ele esteja caindo a velocidade dele é giual a velocidaed mais a aceleração e a posição dele depende dessa velocidade.
    def gravity(self):
        if self.isFalling:
            self.velocidade += self.aceleracao
            self.rect.y += self.velocidade


#função para pular, caso ele não esteja pulando sua velocidade é de 25 e ele não está caindo e está pulando.
    def jump(self):
        if self.isJumping is False:
            self.velocidade = 25
            self.isFalling = False
            self.isJumping = True

#essa função é bastante extensa então comentarei nas linhas
    def update(self) :    #Caso a vida seja maior que 10 por causa de alguma poção ou coisa do gênero ela é setada para 10. Caso seja 0 o jogador morre.
        if self.health > 10:
            self.health = 10
        if self.health == 0:
            self.kill()

        if self.isJumping is False:
            self.isFalling = True
        keys = pygame.key.get_pressed()   #Função do pygame que recebe alguma tecla pressionada pelo usuário
        if keys[pygame.K_d]:  #Caso a tecla seja D ele move-se para a direita
            self.rect.x += 10
            self.image = Imagens["Jogador_direita"]
            self.lado = 1
        if keys[pygame.K_w] and self.velocidade == 0:  #Se a tecla for W ele chama a função de pulo.
            self.jump()
        if keys[pygame.K_a]:  #Se a tecla for a ele anda para a esquerda
            self.rect.x -= 10
            self.image = Imagens["Jogador_esquerda"]
            self.lado = -1

        if self.rect.left < 0:   #Impede que o jogador passe da parte esquerda do limite da tela
            self.rect.left = 0
        if self.rect.right > Comprimento_Tela:  #Impede que passe do lado direito do limite da tela
            self.rect.right = Comprimento_Tela


        if self.rect.bottom >= Altura_Tela and level ==0:    #Caso esteja na primeira fase e caia do limite de altura da tela o jogador toma dano e é teleportado para a posição inicial que deu respawn.
            self.health -= 1
            print(self.health)
            self.rect.x = 80
            self.rect.y = 0

        hites = pygame.sprite.spritecollide(self, vehicles, False)  #Colisão do jogador com o grupo de veículos, o jogador toma 3 de dano.
        if hites:
            if level == 1:
                if self.visible:
                    self.health -= 3
                    self.visible = False
        if self.health <= 0:
            self.kill()

        hits = pygame.sprite.spritecollide(self, enemies, False)  #Colisão com o grupo de inimigos, caso atinja algum inimigo com seu corpo vai tomar 1 de dano.
        if hits:
            if player.visible:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound("Data/paino.WAV"))
                self.health -= 1
                self.visible = False
                if self.health <= 0:
                    self.kill()

        hitou = pygame.sprite.spritecollide(self, boss_spells, False)   #Caso colida com as spells do primeiro boss vai tomar 1 de dano também.
        if hitou:
            if player.visible:
                pygame.mixer.Channel(3).play(pygame.mixer.Sound("Data/paino.WAV"))
                self.health -= 1
                self.visible = False
                if self.health <= 0:
                    self.kill()

        hit_noshowing = pygame.sprite.spritecollide(self, invisible_enemies, False) #Colisão criada para os drones que surgem após o primeiro drone ser derrotado, por isso o nome de invisíveis, essa colisão só funciona se o primeiro drone morrer.
        if hit_noshowing:
            if player.visible:
                if first_droneDown:
                    self.health -= 1
                    self.visible = False



        hit_player_ground = pygame.sprite.spritecollide(self, grounds, False)  #Colisão com o chão, caso a parte de baixo do retângulo do jogador seja menor ou igual a parte de baixo do retângulo do chão a parte de baixo do jogador vai para a parte de cima do chão. Velocidade no eixo y então é zero e ele não está pulando nem caindo.
        if level != 0:
            for g in hit_player_ground:
                self.rect.y += 0
                self.rect.bottom = g.rect.top
                self.isJumping = False
                self.isFalling = False
                self.velocidade = 0
                if self.rect.bottom <= g.rect.bottom:
                    self.rect.bottom = g.rect.top
                else:
                    self.rect.y += self.velocidade

        hit_player_platform = pygame.sprite.spritecollide(self, platforms, False) #As colisões com as plataformas funcionam da mesma forma que com o chão, a parte de baixo do player se mantém na parte de cima das plataformas.
        if level == 0:
            for p in hit_player_platform:
                self.isJumping = False
                self.isFalling = False
                self.velocidade = 0
                self.rect.y += 0
                if self.rect.bottom <= p.rect.bottom:
                    self.rect.bottom = p.rect.top
                else:
                    self.rect.y += self.velocidade

        hit_player_spell = pygame.sprite.spritecollide(self, spells, True) #Colisão do jogador com as magias dos inimigos, o jogador perde 1 de vida toda vez e um som é acionada. As magias somem se acontece a colisão.
        if hit_player_spell:
            pygame.mixer.Channel(4).play(pygame.mixer.Sound("Data/paino.WAV"))
            self.health -= 1
            if self.health == 0:
                self.kill()


        if self.health <=0:
            pygame.mixer.Channel(8).play(pygame.mixer.Sound("Data/game_over_bad_chest.wav"), 0) #Se a vida do jogador chegar a 0 um barulho de game over é acionado

        if self.isJumping:   #Se ele chegar ao pico do pulo a queda é ativada, se isso não acontecer a velocidade depende da aceleração.
            if self.velocidade <= 0:
                self.isJumping = False
                self.isFalling = True
            else:
                self.velocidade -= self.aceleracao
                self.rect.y -= self.velocidade

        hit_player_potion = pygame.sprite.spritecollide(self, pocoes, True) #Colisão do jogador com o grupo das poções, ele recebe 3 de vida, um som é gerado e a poção some.
        if hit_player_potion and level == 0:
            self.health += 3
            if self.health > 10:
                self.health = 10
            pygame.mixer.Channel(2).play(pygame.mixer.Sound("Data/heal.WAV"))



#Função da bala do jogador, se a vida dele for 0 não existe. Para a primeira fase temos um som e para a segunda temos outro. a bala é adicionada a um grupo de sprites de cada nível e a classe de balas criada.
    def shoot(self):
        if self.health != 0:
            if level == 0:
                pygame.mixer.Channel(5).play(pygame.mixer.Sound("Data/foom_0.WAV"))
            elif level == 1:
                pygame.mixer.Channel(5).play(pygame.mixer.Sound("Data/shock.flac"))
            bullet = Bullet(self.rect.centerx, self.rect.top, self.lado, level)
            all_spriteslevel0.add(bullet)
            bullets.add(bullet)
            all_spriteslevel1.add(bullet)
            bullets.add(bullet)

#classe do primeiro boss
class Boss(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Imagens["BossLevel1"]
        self.rect = self.image.get_rect()
        self.rect.x = 2870
        self.rect.y = 35
        self.health = 7
        self.velocidade = 20

#O boss não começa na tela do jogo, ele é spawnado fora da tela e quando o segundo inimigo é morto ele vai em direção a cooredenada marcada.
    def entrada(self):
        if second_enemyDead:
            self.rect.x -= self.velocidade
            if self.rect.x <= 2270:
                self.velocidade = 0

#Função que dita a colisão do boss com as balas do jogador e o som que ele faz quando atingido. Quando a bala o atinge ela some. Vale ressaltar que só toma dano quando o segundo inimigo morre.
    def update(self):
        global level
        if level == 1:
            self.kill()
        hit_boss_bullet = pygame.sprite.spritecollide(self, bullets, True)
        if hit_boss_bullet and second_enemyDead:
            if self.health > 0:
                print(self.health)
                self.health -= 1
                if level == 0:
                    pygame.mixer.Channel(19).play(pygame.mixer.Sound("Data/BossSound.wav"))
        if self.health <= 0:
            self.kill()

#Temos a função que cria os tornados da classe feita lá em cima, adicionando-os ao grupo de sprites do nivel e as spells do boss.
    def spawn(self):
        if self.health > 0 and level == 0:
            tornado = WaterTornado()
            all_spriteslevel0.add(tornado)
            boss_spells.add(tornado)

#Temos aqui a função que atira a Bola de água da classe feita anteriormente.
    def shoot(self):
        if self.health > 0 and level ==0 :
            ball = WaterBall(self.rect.centerx, self.rect.top)
            all_spriteslevel0.add(ball)
            boss_spells.add(ball)

#Criei uma classe para arranjar os estados do jogo
class GameState():
    def __init__(self):
        self.state = 'intro'  #O jogo sempre começa na introdução

    def intro(self):  #Na introdução ele checa se o usuário aperta a tecla Q ou P caso aperte P o jogo se inicia e vamos para a primeira fase, Caso aperte Q o jogo se encerra ali mesmo.
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    pygame.mixer.Channel(6).play(pygame.mixer.Sound("Data/battleThemeA.mp3"), -1) #Musica tema da primeira fase
                    pygame.mixer.Channel(7).stop() #Para a música de introdução do jogo
                    self.state = 'main_game'
            elif event.type == pygame.QUIT: #Esse é o botão X para encerrar a janela
                pygame.quit()
                sys.exit()

        pygame.display.set_caption("Aventuras em Narguiland")  #Nome do jogo que aparece ao canto superior esquerdo
        win.fill((0, 0, 0))  #Pinta a tela toda de preto
        win.blit(canvas2.image, (562,0))  #Coloca a imagem de fundo na coordenada solicitada

        pygame.display.flip()  #desenha as imagens

#Estado do jogo principal
    def main_game(self):
#Variáveis globais criadas no começo do código
        global boss_music
        global delay_shoot
        global level
        global laser_delay
        global first_droneDown
        global can_shoot
        global drones_dead
        global last_drones
        global rocket_delay
        global final_enemyDead
        global threat
        global tornado_delay
        global ball_delay

#Tratador de eventos do teclado
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q: # Q sai do jogo a qualquer momento
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_SPACE: # Barra de Espaço atira a magia do jogador, temos um delay para atirar.
                    if delay_shoot:
                        player.shoot()
                        delay_shoot = False
            elif event.type == pygame.QUIT: #Clicar no X fecha o jogo também
                pygame.quit()
                sys.exit()
            elif event.type == shoot_delay:  #Evento com delay para o primeiro inimigo da primeira fase atirar em um intervalo de tempo, o mesmo delay é utilizado para o jogador tomar dano novamente quando colide com um inimigo.
                player.visible = True
                if player.health != 0:
                    blackmage.shoot()
            elif event.type == magic_delay: #Evento com delay para a bala do jogador, toda vez que o tempo passa a variável de delay é setada.
                delay_shoot = True
            elif event.type == bullet_delay:  #Evento com delay para a torreta atirar as balas, caso todos os drones morram e a posição do jogador seja maior que 1200 ela atira.
                if last_drones and player.rect.x >= 1200:
                    pygame.mixer.Channel(15).play(pygame.mixer.Sound("Data/TurretShot.wav"))  #Som que faz ao atirar
                    turret.shoot()
            elif event.type == rocket_delay:  #Evento com delay para a torreta atirar os foguetes, passado o tempo e caso todos os drones sejam mortor e o jogador esteja em uma posição maior que 1200 ela atira.
                if last_drones and player.rect.x >= 1200:
                    pygame.mixer.Channel(16).play(pygame.mixer.Sound("Data/rlaunch.wav"))
                    turret.fire()
            elif event.type == ball_delay:  #Evento com delay da Bola de Água lançada, se o tempo passou e o boss já fez seu rugido e a posição do jogador é maior que 1200 pode lançar a bola de água.
                if not boss_music and player.rect.x >= 1200:
                    boss1.shoot()
                    if boss1.health > 0:
                        pygame.mixer.Channel(18).play(pygame.mixer.Sound("Data/slimeball.wav"))
            elif event.type == tornado_delay:  #Evento com delay do tornado, se o tempo passou, o boss já rugiu e  a posição do jogador é maior que 1200 pode spawnar.
                if not boss_music and player.rect.x >= 1200:
                    boss1.spawn()
                    if boss1.health > 0:
                        pygame.mixer.Channel(17).play(pygame.mixer.Sound("Data/Spell_01.mp3"))
            elif event.type == laser_delay: #Evento com delay para os drones atirarem, o primeiro drone já começa tirando, os outros três atiram depois que o primeiro morre e os outros dois atiram depois que os 3 morrem.
                drone.shoot()
                if can_shoot:
                    drone1.shoot()
                    drone2.shoot()
                    drone3.shoot()
                    if bike_dead:
                        drone4.shoot()
                        drone5.shoot()

#Dentro do jogo principal o código é dividido por fases
        if level == 0:
            if second_enemyDead and boss_music:  #Caso o segundo inimigo morra e exista a música do boss ele vai fazer um rugido e entrar na tela.
                if boss_music:
                    pygame.mixer.Sound.play(pygame.mixer.Sound("Data/Dragon_Growl_01.WAV"), 0)
                    boss_music = False

            player.gravity()  #chama a gravidade do jogador
            win.fill((0, 0, 0))
            win.blit(canvas.image, (canvas.rect.x - scroll[0], canvas.rect.y - scroll[1]))   #Desenha todas as imagens na tela com um scroll de câmera
            blackmage.virar(player)  #Primeiro inimigo vira de acordo com o jogador


            if boss1.health <=0:    #Se o primeiro chefe morreu vamos para um estado entre fases do jogo
                self.state = 'BetweenFases'
            if player.health <=0:    #Se o jogador morre temos o estado de game over
                self.state = 'game_over'
                pygame.mixer.Channel(6).stop()


            Boss.entrada(boss1)     #Chamada da função para o boss entrar em cena
            ImpHell.move_towards_player(flying_imp, player)    #Chamada de Função que faz o segundo nimigo vir para cima do jogador
            all_spriteslevel0.update()
            for sprite in all_spriteslevel0:   #Para as spites adicionadas no grupo de sprites do level 0 vamos desenhar elas na tela com um scroll de Câmera
                win.blit(sprite.image, (sprite.rect.x - scroll[0], sprite.rect.y - scroll[1]))
            pygame.display.flip()  #Atualiza os desenhos na tela


#Fase 2 do jogo
        if level == 1:

            if final_enemyDead:  #Se o último inimigo morre temos um estado de jogo chamaod de game end onde o jogo acaba.
                pygame.mixer.Channel(13).play(pygame.mixer.Sound("Data/Victory!.wav"),0)
                self.state = 'game_end'

            player.life()  #Chamada de função que dá vida ao jogador quando chega no nível
            player.aceleracao = 2   #Alterei a aceleração do jogador para fins dinâmicos dessa fase nova

            if drone.health <= 0:  #Primeiro drone morre
                first_droneDown = True

            biker.movetowards()   #Motocicleta vai em direção ao jogador

            if first_droneDown:  #Primeiro drone morre, 3 outros vão em direção ao jogador
                Drone.movetowards(drone1, player)
                Drone.movetowards(drone2, player)
                Drone.movetowards(drone3, player)


            pygame.mixer.Channel(6).stop()  #Para a música de fundo da outra fase

            if player.health <= 0:  #Jogador morreu vamos para o estado de game over
                self.state = 'game_over'
            win.fill((0, 0, 0))
            win.blit(canvas4.image,(canvas4.rect.x - scroll[0], canvas4.rect.y - scroll[1] )) #Temos que a imagem de fundo é desenhada com um scroll de Câmera

            player.gravity()  #Chamada de gravidade do jogador
            all_spriteslevel1.update()  #Todos os sprites que foram adicionados a esse grupo e que possuem uma função update são atualizados aqui
            Drone.movetowards(drone, player)  #Primeiro drone move-se em direção ao jogador
            #Update dos outros drones:
            Drone.update(drone1)
            Drone.update(drone2)
            Drone.update(drone3)
            Drone.update(drone4)
            Drone.update(drone5)



            if bike_dead:    #Se a motocicleta morreu 2 drones vão em direção ao jogador
                Drone.movetowards(drone4, player)
                Drone.movetowards(drone5, player)

            if drone4.health == 0 and drone5.health == 0:    #Se os dois últimos drones morrem o jogador recebe 5 de vida e a torreta emite um som.
                if not threat:
                    pygame.mixer.Channel(12).play(pygame.mixer.Sound("Data/optimus_prime_end_of_you.mp3"), 0)
                    threat = True
                    player.health += 5
                    if player.health > 10:
                        player.health = 10
                last_drones = True

            if drone1.health == 0 and drone2.health == 0 and drone3.health == 0:  #Variável dos 3 drones mortos
                drones_dead = True

            for sprit in invisible_enemies:  #Para os inimigos que só aparecem depois que o primeiro drone morre. A imagem só é desenhada depois que ele morre e só podem atirar depois disso.
                if first_droneDown:
                    win.blit(sprit.image, (sprit.rect.x - scroll[0], sprit.rect.y - scroll[1]))
                    can_shoot = True
            for foto in all_spriteslevel1:   #Para as sprites adicionadas no grupo de sprites do nível 1 elas serão desenhadas com scroll de câmera.
                win.blit(foto.image, (foto.rect.x - scroll[0], foto.rect.y - scroll[1]))
            pygame.display.flip()  #Atualiza os desenhos na tela





#Estado game over do jogo:
    def game_over(self):
        self.fimjogo = True
        for event in pygame.event.get(): #Aqui temos apenas dois eventos Q e o botão X da janela para sair do jogo.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        win.fill((0,0,0))
        win.blit(canvas3.image, (562, 0))   #Imagem de fundo desenhada nas seguintes cooredenadas
        pygame.display.flip()

    def betweenfases(self):   #Estado do jogo entre os dois levels
        global level
        player.rect.x = 85      #Atualizei a posição inicial do jogador para a segunda fase
        player.rect.y = 200
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:   #3 eventos, P para continuar no jogo, Q e botão X para sair do jogo.
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                elif event.key == pygame.K_p:
                    self.state = 'main_game'
                    level = 1
                    pygame.mixer.Channel(10).play(pygame.mixer.Sound("Data/Cyberpunk.mp3"), -1)  #Iniciamos a música tema da segunda fase.
            elif event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.mixer.Channel(6).stop()
        win.fill((0, 0, 0))
        win.blit(canvas5.image, (562, 0))   #Desenhamos a imagem de plano de fundo nas coordenadas mostradas.
        pygame.display.flip()


    def game_end(self):  #Estado final do jogo onde tudo acaba
        pygame.mixer.Channel(10).stop()
        for event in pygame.event.get():  #Temos somente os eventos para sair do jogo
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
        win.fill((0,0,0))
        win.blit(canvas6.image, (562, 0))   #Imagem de fim de jogo desenhada
        pygame.display.flip()



    def state_manager(self):  #Tratador dos estados do jogo, começamos na introdução, vamos ao main game, sepois vamos para entre fases e por ultimo game end, caso o jogador morra entramos em game over.
        if self.state == 'intro':
            self.intro()
        if self.state == 'main_game':
            self.main_game()
        if self.state == 'game_over':
            self.game_over()
        if self.state == 'BetweenFases':
            self.betweenfases()
        if self.state == 'game_end':
            self.game_end()




pygame.init()   #Aqui temos as configurações base do jogo onde ele se inicia

pygame.mixer.Channel(7).play(pygame.mixer.Sound("Data/awesomeness.wav"), -1)
game_state = GameState()  #Aqui adicionamos o game_state a classe que tem os códigos principais do jogo e seus estados.
pygame.mixer.set_num_channels(20)  #Número de canais que podemos usar para tocar as músicas
clock = pygame.time.Clock()        #Uma variável clock foi criada como uma função do pyagem de tempo
pygame.display.set_caption("Aventuras em Narguiland")   #Nome do jogo disnponível no canto superior esquerdo

#Criação das plataformas adicionando elas em suas classes, com suas cooredenadas e imagens.
p2 = Platform(62,100,"plat_landing")
p3 = Platform(213,150, "plat_long")
p4 = Platform(1524,235,"plat_cave")
#Adicionamos elas ao grupo de sprites do level 0 para desenharmos elas
all_spriteslevel0.add(p2)
platforms.add(p2)
all_spriteslevel0.add(p3)
platforms.add(p3)
all_spriteslevel0.add(p4)
platforms.add(p4)


#Criamos aqui um grupo de sprites para adicionar inimigos e aqui começamos a adicionar o primeiro inimigo da primeira fase.
enemies = pygame.sprite.Group()
blackmage = BlackMage()
all_spriteslevel0.add(blackmage)
enemies.add(blackmage)

#Criamos o segundo inimigo adicionando ele à classe e ao grupo de inimigos
flying_imp = ImpHell()
all_spriteslevel0.add(flying_imp)
enemies.add(flying_imp)

#Coordenadas iniciais do jogador na primeira fase e adição à classe
player = Player()
player.rect.x = 85
player.rect.y = 0

#adição ao grupo de jogadores e às sprites de level
all_spriteslevel0.add(player)
jogadores.add(player)

#Adição da poção à classe, grupo de poções e sprites do level
pocao_pequena = HealthPotion()
all_spriteslevel0.add(pocao_pequena)
pocoes.add(pocao_pequena)

#Adição do boss à classe, ao grupo de sprites e grupo de inimigos.
boss1 = Boss()
Bosses.add(boss1)
all_spriteslevel0.add(boss1)
enemies.add(boss1)

#Criação da barra de vida e adição ao grupo de sprites
health_bar = HealthBar()
all_spriteslevel0.add(health_bar)

health_bar1 = HealthBar()

#Aqui criamos o chão da segunda fase adicionando ele à classe Ground e setando suas coordenadas, e adicionando ao grupo de sprites. Adicionamos o jogador ao grupo de sprites para desenhar novamente sua imagem  na tela
p5 = Ground(0, 294, "groundFase2")
all_spriteslevel1.add(p5)
grounds.add(p5)
all_spriteslevel1.add(health_bar1)
all_spriteslevel1.add(player)
jogadores.add(player)

#Aqui teremos a adição do primeiro drone à classe, sua localização e adição ao grupo de sprites e inimigos.
drone = Drone()
all_spriteslevel1.add(drone)
enemies.add(drone)
drone.rect.x = 1194
drone.rect.y = 234

#Configuramos os outros drones e colocamos eles no grupo de inimigos invisiveis para aparecerem só depois
drone1 = Drone()
drone2 = Drone()
drone3 = Drone()
drone4 = Drone()
drone5 = Drone()
invisible_enemies.add(drone1)
invisible_enemies.add(drone2)
invisible_enemies.add(drone3)
invisible_enemies.add(drone4)
invisible_enemies.add(drone5)

#Adição do motociclista à classe,grupo de sprites e grupo de veículos
biker = Biker()
vehicles.add(biker)
all_spriteslevel1.add(biker)

#Adição da torreta ao grupo de sprites e classe
turret = FinalTurret()
all_spriteslevel1.add(turret)

#Localizações na tela dos drones
drone1.rect.x = 774
drone1.rect.y = 51

drone2.rect.x = 1068
drone2.rect.y = 162

drone3.rect.x = 1275
drone3.rect.y = 238

drone4.rect.x = 1800
drone4.rect.y = 238

drone5.rect.x = 1800
drone5.rect.y = 150

#Todas as imagens de fundo são usadas aqui, onde adicionamos elas à classe de planos de fundo e usamos as imagens contidas no dicionário.
canvas = BackGround(Imagens["Cenário"])
canvas2 = BackGround(Imagens["TelaInicio"])
canvas3 = BackGround(Imagens["FimdeJogo"])
canvas4 = BackGround(Imagens["SegundaFase"])
canvas5 = BackGround(Imagens["EntreFases"])
canvas6 = BackGround(Imagens["ImagemFinal"])



#Aqui temos a criação dos delays usados como eventos no loop do jogo principal

shoot_delay = pygame.USEREVENT + 2       #Primeiro delay é de 1s e 300 ms para poder atirar novamente
pygame.time.set_timer(shoot_delay,1300)

magic_delay = pygame.USEREVENT + 3        #Segundo delay é de 900 ms para o jogador poder atirar novamente
pygame.time.set_timer(magic_delay,900)

laser_delay = pygame.USEREVENT + 4         #Terceiro delay é para os drones poderem atirar e leva 2 s
pygame.time.set_timer(laser_delay, 2000)

bullet_delay = pygame.USEREVENT + 5        #Quarto delay é para a torreta poder atirar de novo e leva 1 s e 700 ms
pygame.time.set_timer(bullet_delay,1700)

rocket_delay = pygame.USEREVENT + 6        #Quinto delay é para atirar os foguetes e leva 3 s e 500 ms
pygame.time.set_timer(rocket_delay,3500)

tornado_delay = pygame.USEREVENT + 7
pygame.time.set_timer(tornado_delay, 3900)  #Sexto delay é para spawnar os tornados e leva 3 s e 900 ms

ball_delay = pygame.USEREVENT + 8           #O último delay é para o boss atirar a bola de água e leva 2 s e 600 ms
pygame.time.set_timer(ball_delay, 2600)





#Rodamos o jogo por meio desse loop

run = True
while run:

#Como a câmera do jogo iria ficar travada no centro da tela caso nada tivesse sido feito foi necessário criar um scroll de câmera, ou seja, assim que o jogador se movimenta a câmera deve seguir sua movimentação para atualizar a tela.
   #Para fazer essa câmera precisamos criar um "retângulo" em que siga o jogador que tenha mais ou menos as dimensões da metade da tela.

    true_scroll[0] += (player.rect.x - true_scroll[0] - Comprimento_Tela / 2 + 37) / 20
    true_scroll[1] += (player.rect.y - true_scroll[1] - Altura_Tela / 2 + 37) / 20
    scroll = true_scroll.copy()
#Aqui treansformamos os valores em inteiros
    scroll[0] = int(scroll[0])
    scroll[1] = int(scroll[1])
#Caso a tela atinja o máximo e o mínimo da tela ela não pode avançar mais que isso.
    scroll[0] = min(573, scroll[0])
    scroll[1] = min(0, scroll[1])
    scroll[0] = max(-574, scroll[0])
    scroll[1] = max(0, scroll[1])


#Chamamos o tratador de estados da classe para poder rodar o jogo aqui
    game_state.state_manager()
#Configuramos qual o FPS do jogo por meio desse comando
    clock.tick(clock_tick_rate)





