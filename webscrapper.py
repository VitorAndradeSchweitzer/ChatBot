#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Gerador de Dados para Produtos Musicais

Este script gera dados fictícios para preencher o modelo Product:
- name: models.CharField(max_length=100)
- description: models.CharField(max_length=450)
- price: models.FloatField()
- stock: models.IntegerField()
"""

import random
import json
from faker import Faker
from datetime import datetime

# Inicializar Faker para gerar dados realistas
fake = Faker('pt_BR')

class ProductGenerator:
    def __init__(self):
        # Categorias de instrumentos musicais
        self.categories = {
            "cordas": [
                "Violão", "Guitarra", "Baixo", "Violino", "Violoncelo", 
                "Harpa", "Cavaquinho", "Ukulele", "Bandolim", "Banjo"
            ],
            "teclas": [
                "Piano", "Teclado", "Órgão", "Piano Digital", "Sintetizador",
                "Acordeão", "Sanfona", "Teclado Arranger", "Workstation", "Controlador MIDI"
            ],
            "sopro": [
                "Saxofone", "Trompete", "Trombone", "Flauta", "Clarinete",
                "Oboé", "Fagote", "Tuba", "Trompa", "Gaita"
            ],
            "percussão": [
                "Bateria", "Pandeiro", "Tambor", "Atabaque", "Conga",
                "Bongô", "Timbal", "Xilofone", "Marimba", "Vibrafone"
            ],
            "áudio": [
                "Microfone", "Interface de Áudio", "Mixer", "Amplificador", "Caixa de Som",
                "Fone de Ouvido", "Monitor de Áudio", "Processador de Efeitos", "Gravador", "Controladora DJ"
            ],
            "acessórios": [
                "Palheta", "Cordas", "Baqueta", "Estante", "Cabo",
                "Pedal", "Capotraste", "Surdina", "Case", "Afidador"
            ]
        }
        
        # Marcas de instrumentos musicais
        self.brands = [
            "Fender", "Gibson", "Yamaha", "Roland", "Korg", 
            "Shure", "Sennheiser", "Ibanez", "Pearl", "Tama",
            "Martin", "Taylor", "Behringer", "BOSS", "Audio-Technica",
            "Casio", "Kawai", "Nord", "Mapex", "Sabian"
        ]
        
        # Adjetivos para descrições
        self.adjectives = [
            "Profissional", "Premium", "Elétrico", "Acústico", "Digital",
            "Analógico", "Tube", "Vintage", "Moderno", "Clássico",
            "Compacto", "Portátil", "Estúdio", "Ao Vivo", "Practice",
            "Signature", "Custom", "Limited", "Deluxe", "Standard"
        ]
        
        self.products = []
    
    def generate_product_name(self, category):
        """Gera um nome de produto realista"""
        instrument = random.choice(self.categories[category])
        brand = random.choice(self.brands)
        adjective = random.choice(self.adjectives)
        
        # Várias formas de combinar o nome
        name_options = [
            f"{brand} {instrument} {adjective}",
            f"{instrument} {brand} {adjective}",
            f"{adjective} {instrument} {brand}",
            f"{brand} {adjective} {instrument}"
        ]
        
        return random.choice(name_options)
    
    def generate_description(self, name, category):
        """Gera uma descrição realista para o produto"""
        base_descriptions = {
            "cordas": [
                f"Este {name} oferece um timbre excepcional e ótima sustain. Ideal para músicos que buscam qualidade sonora e durabilidade.",
                f"{name} - Perfeito para performances ao vivo e gravações em estúdio. Construção robusta e acabamento impecável.",
                f"Experimente a excelência do {name}. Design ergonômico e resposta tonal equilibrada para todos os estilos musicais."
            ],
            "teclas": [
                f"O {name} conta com sons realistas e recursos avançados para composição e performance. Teclado sensível ao toque.",
                f"{name} - Uma seleção de vozes premium e acompanimentos automáticos para inspirar sua criatividade musical.",
                f"Desfrute da versatilidade do {name}. Interface intuitiva e conectividade completa para integração com DAWs."
            ],
            "sopro": [
                f"O {name} proporciona resposta precisa e entonação perfeita. Construído com materiais de alta qualidade para durabilidade.",
                f"{name} - Instrumento de sopro com afinação precisa e tom rico. Ideal para estudantes e profissionais.",
                f"Descubra o som característico do {name}. Design ergonômico que facilita a execução e proporciona conforto."
            ],
            "percussão": [
                f"O {name} oferece projeção poderosa e tons bem definidos. Hardware resistente para performances intensas.",
                f"{name} - Conjunto de percussão com excelente resposta e durabilidade. Perfect para estúdio e palco.",
                f"Experimente a qualidade do {name}. Acabamento premium e sonoridade excepcional para todas as aplicações."
            ],
            "áudio": [
                f"O {name} proporciona captação precisa e reprodução fiel. Ideal para gravação, mixagem e masterização.",
                f"{name} - Equipamento de áudio profissional com recursos avançados e construção robusta para uso intensivo.",
                f"Desfrute da qualidade de áudio do {name}. Design inovador e tecnologia de ponta para resultados superiores."
            ],
            "acessórios": [
                f"O {name} é fabricado com materiais de alta qualidade para durabilidade e desempenho excepcional.",
                f"{name} - Acessório essencial para músicos, oferecendo confiabilidade e desempenho superior em todas as situações.",
                f"Melhore sua experiência musical com o {name}. Design funcional e materiais premium para resultados profissionais."
            ]
        }
        
        return random.choice(base_descriptions[category])
    
    def generate_price(self, category):
        """Gera um preço realista baseado na categoria"""
        base_prices = {
            "cordas": (300, 5000),
            "teclas": (800, 15000),
            "sopro": (500, 8000),
            "percussão": (400, 10000),
            "áudio": (200, 8000),
            "acessórios": (20, 1000)
        }
        
        min_price, max_price = base_prices[category]
        # Preços tendem a ser números que terminam em 9 ou 0 (prática comum de pricing)
        price = random.randint(min_price, max_price)
        # Ajusta para terminar com 9 ou 0 (ex: 299, 450)
        last_digit = price % 10
        if last_digit not in [0, 9]:
            price = price - last_digit + (9 if random.random() > 0.5 else 0)
        
        return float(price)
    
    def generate_stock(self):
        """Gera uma quantidade de estoque realista"""
        # Distribuição: maioria com estoque, alguns com pouco, alguns sem
        r = random.random()
        if r < 0.7:  # 70% com estoque bom
            return random.randint(5, 50)
        elif r < 0.9:  # 20% com estoque baixo
            return random.randint(1, 4)
        else:  # 10% sem estoque
            return 0
    
    def generate_products(self, num_products=100):
        """Gera uma lista de produtos"""
        print(f"Gerando {num_products} produtos musicais...")
        
        # Distribuir produtos por categoria
        categories = list(self.categories.keys())
        weights = [0.25, 0.20, 0.15, 0.15, 0.15, 0.10]  # Probabilidades para cada categoria
        
        for i in range(num_products):
            # Selecionar categoria baseado nos pesos
            category = random.choices(categories, weights=weights, k=1)[0]
            
            name = self.generate_product_name(category)
            description = self.generate_description(name, category)
            price = self.generate_price(category)
            stock = self.generate_stock()
            
            product = {
                "name": name,
                "description": description,
                "price": price,
                "stock": stock,
                "category": category
            }
            
            self.products.append(product)
            
            if (i + 1) % 10 == 0:
                print(f"{i + 1} produtos gerados...")
        
        print(f"Geração concluída! {len(self.products)} produtos criados.")
        return self.products
    
    def save_to_json(self, filename="products_data.json"):
        """Salva os produtos em um arquivo JSON"""
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)
        print(f"Dados salvos em {filename}")
    
    def save_to_csv(self, filename="products_data.csv"):
        """Salva os produtos em um arquivo CSV"""
        import csv
        
        with open(filename, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            # Escrever cabeçalho
            writer.writerow(['name', 'description', 'price', 'stock', 'category'])
            
            # Escrever dados
            for product in self.products:
                writer.writerow([
                    product['name'],
                    product['description'],
                    product['price'],
                    product['stock'],
                    product['category']
                ])
        
        print(f"Dados salvos em {filename}")
    
    def print_sample(self, num_samples=5):
        """Imprime uma amostra dos produtos gerados"""
        print("\n" + "="*80)
        print("AMOSTRA DOS PRODUTOS GERADOS")
        print("="*80)
        
        for i, product in enumerate(self.products[:num_samples]):
            print(f"\n--- Produto {i+1} ---")
            print(f"Nome: {product['name']}")
            print(f"Descrição: {product['description']}")
            print(f"Preço: R$ {product['price']:,.2f}")
            print(f"Estoque: {product['stock']} unidades")
            print(f"Categoria: {product['category']}")
    
    def generate_django_fixture(self, filename="products_fixture.json"):
        """Gera um fixture no formato do Django"""
        fixture_data = []
        for i, product in enumerate(self.products):
            fixture_data.append({
                "model": "store.product",
                "pk": i + 1,
                "fields": {
                    "name": product['name'],
                    "description": product['description'],
                    "price": product['price'],
                    "stock": product['stock'],
                    "created_at": datetime.now().isoformat(),
                    "updated_at": datetime.now().isoformat()
                }
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(fixture_data, f, ensure_ascii=False, indent=2)
        
        print(f"Fixture do Django salvo em {filename}")

def main():
    """Função principal"""
    print("GERADOR DE PRODUTOS MUSICAIS")
    print("="*50)
    
    # Inicializar gerador
    generator = ProductGenerator()
    
    # Gerar produtos
    num_products = int(input("Quantos produtos deseja gerar? (Padrão: 100) ") or "100")
    products = generator.generate_products(num_products)
    
    # Mostrar amostra
    generator.print_sample(5)
    
    # Salvar dados
    generator.save_to_json()
    generator.save_to_csv()
    generator.generate_django_fixture()
    
    # Estatísticas
    categories_count = {}
    for product in products:
        category = product['category']
        categories_count[category] = categories_count.get(category, 0) + 1
    
    print("\n" + "="*50)
    print("ESTATÍSTICAS:")
    print("="*50)
    for category, count in categories_count.items():
        print(f"{category}: {count} produtos")
    
    total_value = sum(product['price'] * product['stock'] for product in products)
    print(f"\nValor total em estoque: R$ {total_value:,.2f}")
    
    print("\nArquivos gerados:")
    print("- products_data.json (dados completos em JSON)")
    print("- products_data.csv (dados em formato CSV)")
    print("- products_fixture.json (fixture para Django)")

if __name__ == "__main__":
    main()