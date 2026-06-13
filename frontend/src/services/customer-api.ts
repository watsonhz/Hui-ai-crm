/** Customer CRUD API service — typed methods for every endpoint in the API spec. */

import { get, post, put, del } from './api-client';
import type {
  Customer,
  CreateCustomerDto,
  UpdateCustomerDto,
  CustomerListParams,
  PaginatedResponse,
} from '@/types/customer';

const BASE = '/customers';

export const customerApi = {
  getList(params: CustomerListParams = {}) {
    return get<PaginatedResponse<Customer>>(BASE, params as Record<string, unknown>);
  },

  getById(id: number) {
    return get<Customer>(`${BASE}/${id}`);
  },

  create(data: CreateCustomerDto) {
    return post<Customer>(BASE, data);
  },

  update(id: number, data: UpdateCustomerDto) {
    return put<Customer>(`${BASE}/${id}`, data);
  },

  remove(id: number) {
    return del<void>(`${BASE}/${id}`);
  },
};
