-- Товары
CREATE TABLE public.products (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50)
);
-- Цены
CREATE TABLE public.prices (
    id SERIAL PRIMARY KEY,
    product_id INTEGER REFERENCES public.products(id) ON DELETE CASCADE,
    price NUMERIC(10, 2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
-- Поставщики
CREATE TABLE public.suppliers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    product_id INTEGER REFERENCES public.products(id) ON DELETE CASCADE
);