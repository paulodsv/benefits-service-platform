-- init schema for benefits example
CREATE TABLE IF NOT EXISTS companies (
  id SERIAL PRIMARY KEY,
  name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS employees (
  id SERIAL PRIMARY KEY,
  company_id INT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  name TEXT NOT NULL,
  document TEXT,
  status TEXT DEFAULT 'active',
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS balances (
  id SERIAL PRIMARY KEY,
  employee_id INT NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
  benefit_type TEXT NOT NULL,
  amount NUMERIC(12,2) NOT NULL DEFAULT 0,
  updated_at TIMESTAMP DEFAULT now(),
  UNIQUE (employee_id, benefit_type)
);

CREATE TABLE IF NOT EXISTS loads (
  id SERIAL PRIMARY KEY,
  company_id INT NOT NULL REFERENCES companies(id) ON DELETE CASCADE,
  total_items INT NOT NULL,
  amount_total NUMERIC(12,2) NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT now()
);

CREATE TABLE IF NOT EXISTS load_items (
  id SERIAL PRIMARY KEY,
  load_id INT NOT NULL REFERENCES loads(id) ON DELETE CASCADE,
  employee_id INT NOT NULL REFERENCES employees(id) ON DELETE CASCADE,
  amount NUMERIC(12,2) NOT NULL,
  status TEXT NOT NULL DEFAULT 'pending'
);

-- sample data
INSERT INTO companies (name) VALUES ('Empresa X') ON CONFLICT DO NOTHING;
INSERT INTO employees (company_id, name) VALUES (1, 'Paulo Teste') ON CONFLICT DO NOTHING;
