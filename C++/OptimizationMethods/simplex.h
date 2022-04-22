#pragma once
#include "vector_utils.h"
#include "matrix_utils.h"
#include "numeric_utils.h"
#include <iomanip>
#include <string>
////////////////////
/// Lab. work #5 ///
////////////////////
namespace sm
{
	constexpr auto EQUAL = 0;
	constexpr auto LESS_EQUAL = -1;
	constexpr auto MORE_EQUAL = 1;

#define SIMPLEX_MAX  0
#define SIMPLEX_MIN  1

	class simplex
	{
	private:
		/// <summary>
		/// ������ ������ � ���������� � ������� �����������
		/// </summary>
		std::vector<int> ineqs;

		/// <summary>
		/// ������ �������� ���������� ������� ������ � ������� ������, ����������� ��
		/// </summary>
		std::vector<int> f_mod_args;

		/// <summary>
		///������� ������������ ����������
		/// </summary>
		std::vector<int> natural_args_ids;

		/// <summary>
		///������� ����������, �� ���������� ��������������
		/// </summary>
		std::vector<int> artificial_args_ids;

		/// <summary>
		/// ������ �������� ������� �������� ���������� 
		/// </summary>
		std::vector<int> basis_args;

		/// <summary>
		/// �������� �������
		/// </summary>
		mat_mn symplex_t;

		/// <summary>
		/// ������� �����������
		/// </summary>
		mat_mn bounds_m;

		/// <summary>
		/// ������ �����������
		/// </summary>
		vec_n bounds_v;

		/// <summary>
		/// ������ ����������
		/// </summary>
		vec_n prices_v;

		/// <summary>
		/// ����� ������ �������
		/// </summary>
		int mode = SIMPLEX_MAX;

		/// <summary>
		/// ��������� ������������� �������� �������� �����. ����������� ��������������� 
		/// ��������-��������� � ��������� ������ �� � ��������� �� 1:n-1.
		/// ���� ������� ������� ���� ��������������, �� ��������� ��� ��������� ������.
		/// ���� ����� ��������� �� 1:n-1 � ��������� ������ ��� �������������, �� ��������� 
		/// �� ����������������� ������ �� �������� ������������� ������, ������� �� ��������
		/// ��������������.
		/// </summary>
		/// <param name="A">�� ������a</param>
		/// <param name="mode"></param>
		/// <returns></returns>
		bool is_plan_optimal()const
		{
			/// <summary>
			/// ��������� �������� ��������� ������ �������-���������
			/// �� ���������������. ���� ��� ������������, �� ���� ���������.
			/// </summary>

			const vec_n& row = symplex_t[symplex_t.size() - 1];

			bool opt = true;

			for (int i = 0; i < row.size() - 1; i++)
			{
				if (row[i] < 0)
				{
					opt = false;
					break;
				}
			}

			/// <summary>
			/// ���� �� �������������� ������� �������, �� ����� ������ �������������
			/// ��������� �������� �� ���������������� ������������ ������ ��������-��������� 
			/// </summary>

			if (is_target_f_modified())
			{
				if (!opt)
				{
					return opt;
				}
				const vec_n& row_ = symplex_t[symplex_t.size() - 2];

				for (const auto& id : natural_args_ids)
				{
					if (row_[id] < 0)
					{
						opt = false;
						break;
					}
				}
			}

			return opt;
		}

		/// <summary>
		/// ���������� ������� �������. ����� ��������� ������ ��������-��������� ���� ����������� �� ������ 
		/// ������������� �������. ���� ������� ������� ���� �������������� � ����� ��������� ������ ��� �������������
		/// ���������, �� ����� ������� ����� ��������� ����� ������ ��� ��������� ������������� ������, ������� ��
		/// �������� ��������������.
		/// </summary>
		/// <param name="A"></param>
		/// <returns></returns>
		int get_main_col()const
		{
			const vec_n& row = symplex_t[symplex_t.size() - 1];

			double delta = 0;

			int    index = -1;

			for (int i = 0; i < row.size() - 1; i++)
			{
				if (row[i] >= delta)
				{
					continue;
				}
				delta = row[i];
				index = i;
			}

			if (is_target_f_modified() && index == -1)
			{
				const vec_n& row_add = symplex_t[symplex_t.size() - 2];

				for (const auto& id : natural_args_ids)
				{
					if (row_add[id] >= delta)
					{
						continue;
					}
					delta = row_add[id];
					index = id;
				}
			}
			return index;
		}

		/// <summary>
		/// ���������� ������� ������ 
		/// </summary>
		/// <param name="symplex_col">������� �������</param>
		/// <param name="A">�� �������</param>
		/// <returns></returns>
		int get_main_row(const int symplex_col)const
		{
			double delta = 1e12;

			int index = -1;

			double a_ik;

			int b_index = symplex_t[0].size() - 1;

			int cntr = 0;

			int rows_n = is_target_f_modified() ? symplex_t.size() - 2 : symplex_t.size() - 1;

			for (int i = 0; i < rows_n; i++)
			{
				a_ik = symplex_t[i][symplex_col];

				if (a_ik < 0)
				{
					cntr++;
					continue;
				}
				if (symplex_t[i][b_index] / a_ik > delta)
				{
					continue;
				}
				delta = symplex_t[i][b_index] / a_ik;
				index = i;
			}

			return index;
		}

		/// <summary>
		/// ������ ����������� �������� ������
		/// </summary>
		/// <param name="ineq_id"></param>
		/// <param name="_ineq"></param>
		/// <param name="col_index"></param>
		/// <param name="col_index_aditional"></param>
		bool build_virtual_basis_col(const int ineq_id, const int _ineq, int& col_index, int& col_index_aditional)
		{
			if (_ineq == EQUAL)
			{
				for (int row = 0; row < symplex_t.size(); row++)
				{
					if (row == ineq_id)
					{
						symplex_t[row].push_back(1.0);
						continue;
					}
					symplex_t[row].push_back(0.0);
				}

				col_index = symplex_t[0].size() - 1;

				col_index_aditional = symplex_t[0].size() - 1;

				return true;
			}

			if (_ineq == MORE_EQUAL)
			{
				for (int row = 0; row < symplex_t.size(); row++)
				{
					if (row == ineq_id)
					{
						symplex_t[row].push_back(-1.0);

						symplex_t[row].push_back(1.0);

						continue;
					}

					symplex_t[row].push_back(0.0);

					symplex_t[row].push_back(0.0);
				}

				col_index_aditional = symplex_t[0].size() - 1;

				col_index = symplex_t[0].size() - 2;

				return false;
			}

			for (int row = 0; row < symplex_t.size(); row++)
			{
				if (row == ineq_id)
				{
					symplex_t[row].push_back(1.0);
					continue;
				}
				symplex_t[row].push_back(0.0);
			}

			col_index_aditional = -1;

			col_index = symplex_t[0].size() - 1;

			return true;
		}

		/// <summary>
		/// ������ �� ������� ��� ������ ����:
		/// ������� ������� ����������:
		///		|u 0 0|	
		/// A = |0 v 0|
		///		|0 0 w|
		/// ������ �����������
		///		|a|	
		/// b = |d|
		///		|f|
		/// � -������������ ������� ������� 
		/// f = (x,c)->extr
		///	|u 0 0|   |x| <= |b|
		/// |0 v 0| * |x| >= |f|
		///	|0 0 w|   |x| =  |d|
		/// 
		///  �� ������� �� A,b,c ����������
		/// </summary>
		/// <param name="A"> Ax <= b   -> (A|I)(x|w) = b </param>
		/// <param name="c"> (c,x) ->((-c|0),(x|w)) </param>
		/// <param name="ineq"> ���� ����������� =, >=, <= </param>
		/// <param name="b"></param>
		///( A|I)  b
		///(-c|0)  F(x,c)
		void build_symplex_table()
		{
			symplex_t = bounds_m;

			///
			/// ���� ����� ������� b ���� ������������� ��������, �� ��������������� ������
			/// ������� ����������� �������� �� ���� ���� � ������ ���� ���������
			///
			for (int row = 0; row < symplex_t.size(); row++)
			{
				if (bounds_v[row] >= 0)
				{
					continue;
				}

				ineqs[row] *= -1;

				bounds_v[row] *= -1;

				symplex_t[row] = symplex_t[row] * (-1.0);
			}


			for (int i = 0; i < prices_v.size(); i++)
			{
				natural_args_ids.push_back(i);
			}
			/// <summary>
			/// ���������� ������������� ������
			/// </summary>
			int basis_arg_id;
			int basis_arg_id_add;
			for (int ineq_id = 0; ineq_id < ineqs.size(); ineq_id++)
			{
				build_virtual_basis_col(ineq_id, ineqs[ineq_id], basis_arg_id, basis_arg_id_add);

				natural_args_ids.push_back(basis_arg_id);

				if (basis_arg_id_add != -1)
				{
					basis_args.push_back(basis_arg_id_add);
					f_mod_args.push_back(basis_arg_id_add);
					artificial_args_ids.push_back(basis_arg_id_add);
					continue;
				}

				basis_args.push_back(basis_arg_id);
			}

			/// <summary>
			/// ������� ������� �����������
			/// </summary>

			for (int row = 0; row < symplex_t.size(); row++)
			{
				symplex_t[row].push_back(bounds_v[row]);
			}

			/// <summary>
			/// ���������� �������� ���������
			/// </summary>

			vec_n s_deltas(symplex_t[0].size());

			if (mode == SIMPLEX_MAX)
			{
				for (int j = 0; j < s_deltas.size(); j++)
				{
					s_deltas[j] = j < prices_v.size() ? -prices_v[j] : 0.0;
				}
			}
			else
			{
				for (int j = 0; j < s_deltas.size(); j++)
				{
					s_deltas[j] = j < prices_v.size() ? prices_v[j] : 0.0;
				}
			}

			symplex_t.push_back(s_deltas);

			/// <summary>
			/// ���� ������� �������� �� ���� ��������������
			/// </summary>

			if (!is_target_f_modified())
			{
				return;
			}

			/// <summary>
			/// ���� �� �� ����...
			/// </summary>
			vec_n s_deltas_add(symplex_t[0].size());

			for (int j = 0; j < f_mod_args.size(); j++)
			{
				s_deltas_add[f_mod_args[j]] = 1.0;
			}

			symplex_t.push_back(s_deltas_add);
		}

		bool exclude_mod_args()
		{
			if (!is_target_f_modified())
			{
				return false;
			}

			int last_row_id = symplex_t.size() - 1;

			for (int i = 0; i < f_mod_args.size(); i++)
			{
				for (int row = 0; row < symplex_t.size(); row++)
				{
					if (symplex_t[row][f_mod_args[i]] != 0)
					{
						double arg = symplex_t[last_row_id][f_mod_args[i]] / symplex_t[row][f_mod_args[i]];

						symplex_t[last_row_id] = symplex_t[last_row_id] - arg * symplex_t[row];

						break;
					}
				}
			}

			return true;
		}

		bool validate_solution()const
		{
			double val = 0;

			int n_rows = is_target_f_modified() ? symplex_t.size() - 2 : symplex_t.size() - 1;

			int n_cols = symplex_t[0].size() - 1;

			for (int i = 0; i < basis_args.size(); i++)
			{
				if (basis_args[i] < natural_args_n())
				{
					val += symplex_t[i][n_cols] * prices_v[basis_args[i]];
				}
			}
			if (mode == SIMPLEX_MAX)
			{
				if (abs(val - symplex_t[n_rows][n_cols]) < 1e-5)
				{
					if (is_target_f_modified())
					{
						return true & (abs(symplex_t[symplex_t.size() - 1][symplex_t[0].size() - 1]) < 1e-5);
					}

					return true;
				}
			}
			if (abs(val + symplex_t[n_rows][n_cols]) < 1e-5)
			{
				if (is_target_f_modified())
				{
					return true & (abs(symplex_t[symplex_t.size() - 1][symplex_t[0].size() - 1]) < 1e-5);
				}

				return true;
			}
			return false;
		}

	public:

		/// <summary>
		/// ���������� ���������� �������� ������� �������
		/// </summary>
		int natural_args_n()const
		{
			return prices_v.size();
		}

		inline const mat_mn& bounds_matrix()const
		{
			return bounds_m;
		}

		inline const vec_n& bounds_coeffs()const
		{
			return bounds_v;
		}

		inline const vec_n& prices_coeffs()const
		{
			return prices_v;
		}

		inline const std::vector<int>& inequations()const
		{
			return ineqs;
		};

		inline const std::vector<int>& basis_argsuments()const
		{
			return basis_args;
		};

		inline const mat_mn& table() const { return symplex_t; };

		inline bool is_target_f_modified()const
		{
			return f_mod_args.size() != 0;
		}

		friend std::ostream& operator<<(std::ostream& stream, const simplex& s);
		/// <summary>
		/// ������� ������� ������� �� ������� ��� �� ������������� ����������
		/// </summary>
		/// <param name="A">�� �������</param>
		/// <param name="basis">������ �������� ����������</param>
		/// <param name="n_agrs">���������� �������� ����������</param>
		/// <returns></returns>
		vec_n current_symplex_solution(const bool only_natural_args = false)const
		{
			vec_n solution(only_natural_args ? natural_args_n() : symplex_t[0].size() - 1);

			for (int i = 0; i < basis_args.size(); i++)
			{
				if (basis_args[i] >= solution.size())
				{
					continue;
				}

				solution[basis_args[i]] = symplex_t[i][symplex_t[0].size() - 1];
			}
			return solution;
		}

		vec_n solve(const int mode = SIMPLEX_MAX)
		{
			this->mode = mode;
			
			std::cout << "Symplex problem type: " << ((mode == SIMPLEX_MAX) ? "max\n" : "min\n");

			build_symplex_table();

			vec_n solution;

			double a_ik;

			int main_row;

			int main_col;

			std::cout << "Start symplex table:" << std::endl;

			std::cout << *this;

			if (exclude_mod_args())
			{
				// ������ ����, ���� ������ ������ �������� ���� ���������(���� �������) ����������
				std::cout << "Symplex table after args exclude:" << std::endl;

				std::cout << *this;
			}

			while (!is_plan_optimal())
			{
				main_col = get_main_col();

				if (main_col == -1)
				{
					break;
				}

				main_row = get_main_row(main_col);

				if (main_row == -1)
				{
					/// ������������� ���������� ������� ������ ���������������� � ���, ��� ������� ������ ������������
					std::cout << "Unable to get main row. Symplex is probably boundless...\n";
					solution.clear();
					return solution;
				}

				basis_args[main_row] = main_col;

				a_ik = symplex_t[main_row][main_col];

				symplex_t[main_row] = symplex_t[main_row] * (1.0 / a_ik);

				for (int i = 0; i < symplex_t.size(); i++)
				{
					if (i == main_row)
					{
						continue;
					}
					symplex_t[i] = symplex_t[i] - symplex_t[i][main_col] * symplex_t[main_row];
				}
				solution = current_symplex_solution();

#if _DEBUG
				std::cout << "a_main { " << main_row + 1 << ", " << main_col + 1 << " } = " << str_rational(a_ik) << std::endl;
				std::cout << *this;
				std::cout << "current_solution" << str_rational(solution) << std::endl;
				std::cout << std::endl;
#endif
			}
			if (validate_solution())
			{
				solution = current_symplex_solution(true);
				/// ������������ ������
				std::cout << "solution : " << str_rational(solution) << "\n";
				return solution;
			}
			std::cout << "Symplex is unresolvable\n";
			/// �������� ������� ������� �� ����� �� �������� �� ���������� �����
			solution.clear();
			return solution;
		}

		simplex(const mat_mn& a, const vec_n& c, const std::vector<int>& _ineq, const vec_n& b)
		{
			if (b.size() != _ineq.size())
			{
				throw std::runtime_error("Error symplex creation :: b.size() != inequation.size()");
			}
			if (a.size() != _ineq.size())
			{
				throw std::runtime_error("Error symplex creation :: A.rows_number() != inequation.size()");
			}

			if (a[0].size() != c.size())
			{
				throw std::runtime_error("Error symplex creation :: A.cols_number() != price_coeffs.size()");
			}

			bounds_v = b;

			bounds_m = a;

			prices_v = c;

			ineqs = std::vector<int>(_ineq);
		}

		simplex(const mat_mn& a, const vec_n& c, const vec_n& b)
		{
			if (a.size() != b.size())
			{
				throw std::runtime_error("Error symplex creation :: A.rows_number() != bouns_coeffs.size()");
			}

			if (a[0].size() != c.size())
			{
				throw std::runtime_error("Error symplex creation :: A.cols_number() != price_coeffs.size()");
			}

			std::vector<int> _ineq;

			for (int i = 0; i < b.size(); i++)
			{
				_ineq.push_back(LESS_EQUAL);
			}

			bounds_v = b;

			bounds_m = a;

			prices_v = c;

			ineqs = std::vector<int>(_ineq);
		}
	};
	std::ostream& operator<<(std::ostream& stream, const simplex& s)
	{
		/// <summary>
		///	  (x,w)	
		/// w (A|I)  b
		///   (c|i)  F(x,c)
		/// </summary>
		/// <param name="a"></param>
		/// <param name="b"></param>
		/// <param name="c"></param>

		const  mat_mn& A = s.table();

		const bool targeFuncMod = s.is_target_f_modified();

		const std::vector<int>& basis_args = s.basis_argsuments();

		if (A.size() == 0)
		{
			return stream;
		}

		const char separator = ' ';

		const int colom_title_w = 6;

		const int colom_w = 12;

		stream << std::left << std::setw(colom_title_w) << std::setfill(separator) << "";

		int i = 0;

		for (; i < A[0].size() - 1; i++)
		{
			stream << std::left << std::setw(colom_w) << std::setfill(separator) << "| x " + std::to_string(i + 1);
		}

		stream << std::left << std::setw(colom_w) << std::setfill(separator) << "| b";

		stream << std::endl;

		int n_row = -1;

		for (auto const& row : A)
		{
			n_row++;

			if (targeFuncMod)
			{
				if (n_row == A.size() - 2)
				{
					stream << std::left << std::setw(colom_title_w) << std::setfill(separator) << " d0 ";
				}
				else if (n_row == A.size() - 1)
				{
					stream << std::left << std::setw(colom_title_w) << std::setfill(separator) << " d1 ";
				}
				else
				{
					stream << std::left << std::setw(colom_title_w) << std::setfill(separator) << " x " + std::to_string(basis_args[n_row] + 1);
				}
			}
			else
			{
				if (n_row == A.size() - 1)
				{
					stream << std::left << std::setw(colom_title_w) << std::setfill(separator) << " d ";
				}
				else
				{
					stream << std::left << std::setw(colom_title_w) << std::setfill(separator) << " x " + std::to_string(basis_args[n_row] + 1);
				}
			}

			for (int col = 0; col < row.size(); col++)
			{
				if (row[col] >= 0)
				{
					stream << std::left << std::setw(colom_w) << std::setfill(separator) << "| " + str_rational(row[col]);
					continue;
				}
				stream << std::left << std::setw(colom_w) << std::setfill(separator) << "|" + str_rational(row[col]);
			}

			stream << std::endl;
		}
		stream << std::endl;

		return stream;
	}
}
