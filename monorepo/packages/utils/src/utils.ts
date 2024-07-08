import {v4 as uuidv4} from 'uuid';

export function sum(a: number, b: number): number {
  return a + b;
}

export function generateUUID(): string {
  return uuidv4();
}
