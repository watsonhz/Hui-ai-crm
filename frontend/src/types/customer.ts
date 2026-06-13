/** TypeScript types matching the API spec and database schema. */

export type CustomerLevel = 'A' | 'B' | 'C' | 'D';

export type CustomerStatus = '潜在' | '意向' | '谈判' | '成交' | '流失';

export type FunnelStage = '线索' | '初访' | '需求' | '报价' | '谈判' | '成交' | '丢单';

export interface Customer {
  id: number;
  name: string;
  company: string;
  industry: string;
  phone: string;
  email: string;
  source: string;
  level: CustomerLevel;
  status: CustomerStatus;
  owner_id: number | null;
  created_at: string;
  updated_at: string;
}

export interface Contact {
  id: number;
  customer_id: number;
  name: string;
  title: string;
  phone: string;
  email: string;
  is_primary: boolean;
}

export interface SalesFunnel {
  id: number;
  customer_id: number;
  stage: FunnelStage;
  amount: number;
  probability: number;
  expected_close: string | null;
  notes: string;
}

/** Request DTOs */
export interface CreateCustomerDto {
  name: string;
  company?: string;
  industry?: string;
  phone?: string;
  email?: string;
  source?: string;
  level?: CustomerLevel;
  status?: CustomerStatus;
}

export interface UpdateCustomerDto extends Partial<CreateCustomerDto> {}

export interface CustomerListParams {
  page?: number;
  page_size?: number;
  name?: string;
  company?: string;
  status?: CustomerStatus;
  level?: CustomerLevel;
  source?: string;
  sort?: 'created_at' | '-created_at';
}

/** API response shapes */
export interface PaginatedResponse<T> {
  items: T[];
  total: number;
  page: number;
  page_size: number;
}

export interface ApiResponse<T> {
  code: number;
  message: string;
  data: T;
}
