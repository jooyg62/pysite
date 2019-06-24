import math

from django.db.models import Max, Q
from django.http import HttpResponseRedirect, HttpResponseServerError, Http404
from django.shortcuts import render

from board.models import Board
from user.models import User


def list(request):
    data = {}

    # 1. 전체 조회
    board_list = Board.objects.all().order_by('-id')

    # 2. 검색 조건 조회
    kwd = request.GET.get('kwd', '')

    if kwd:
        board_list = board_list.filter(Q(title__icontains=kwd) | Q(contents__icontains=kwd))

    # 3. 게시물 번호 매기기
    for index, board in enumerate(board_list):
        board.no = len(board_list) - index

    # 4. 페이징 처리 정보
    #####################################################################################
    #   cur_paging_num              :   현재 보고 있는 페이지 넘버
    #   tot_board_count             :   전체 게시물 수
    #   page_per_size               :   페이지당 게시물 개수
    #   tot_paging_size             :   최대로 넘길 수 있는 페이지 넘버
    #   paging_num_size             :   화면에 몇개의 페이징을 줄 것 인지.(1 2 3 4 5)
    #   start_view_paging_num       :   시작 페이징 번호
    #   is_pre_page                 :   이전 페이징으로 갈수 있는지 여부
    #   is_after_page               :   이후 페이징으로 갈수 있는지 여부
    #   paging_list                 :   페이징 번호 리스트 (<< 1 2 3 4 5 >>)
    ######################################################################################
    cur_paging_num = int(request.GET.get('cur_paging_num', 1))
    tot_board_count = len(board_list)

    page_per_size = 2
    tot_paging_size = int((tot_board_count-1) / page_per_size) + 1
    paging_num_size = 5
    start_view_paging_num = int((cur_paging_num-1) / paging_num_size) * paging_num_size + 1
    is_pre_page = True if cur_paging_num > 1 else False
    is_after_page = True if tot_paging_size > cur_paging_num else False
    paging_list = get_paging_list(paging_num_size, start_view_paging_num)

    start = (cur_paging_num-1) * page_per_size
    board_list = board_list[start:start+page_per_size]

    # 5. 데이터 담기
    data['kwd'] = kwd

    data['board_list'] = board_list

    data['cur_paging_num'] = cur_paging_num
    data['tot_board_count'] = tot_board_count
    data['page_per_size'] = page_per_size
    data['tot_paging_size'] = tot_paging_size
    data['paging_num_size'] = paging_num_size
    data['start_view_paging_num'] = start_view_paging_num
    data['is_pre_page'] = is_pre_page
    data['is_after_page'] = is_after_page
    data['paging_list'] = paging_list
    data['start'] = start

    return render(request, 'board/list.html', data)


def view(request, id=0):
    data = {}

    # 1. 키워드, 페이지 히스토리 전달
    kwd = request.GET.get('kwd', '')
    cur_paging_num = request.GET.get('cur_paging_num', '')

    data['kwd'] = kwd
    data['cur_paging_num'] = cur_paging_num

    # 2. 게시물 조회
    board = Board.objects.get(id=id)
    data['board'] = board

    # 3. 조회 hit 증가
    board.hit += 1
    board.save()

    return render(request, 'board/view.html', data)


def modify(request, id=0):
    data = {}

    # 1. 키워드, 페이지 히스토리 전달
    kwd = request.GET.get('kwd', '')
    cur_paging_num = request.GET.get('cur_paging_num', '')

    data['kwd'] = kwd
    data['cur_paging_num'] = cur_paging_num

    # 2. 게시물 조회
    board = Board.objects.get(id=id)
    data['board'] = board

    return render(request, 'board/modify.html', data)


def update(request, id=0):

    # 1. 키워드, 페이지 히스토리 전달
    kwd = request.GET.get('kwd', '')
    cur_paging_num = request.GET.get('cur_paging_num', '')

    # 2. 게시물 수정
    board = Board.objects.get(id=id)
    board.title = request.POST['title']
    board.contents = request.POST['content']

    board.save()

    return HttpResponseRedirect('/board?kwd=' + kwd + '&cur_paging_num=' + cur_paging_num)


def write(request):
    data = {}

    # 키워드, 페이지 히스토리 전달
    kwd = request.GET.get('kwd', '')
    cur_paging_num = request.GET.get('cur_paging_num', '')

    data['kwd'] = kwd
    data['cur_paging_num'] = cur_paging_num

    return render(request, 'board/write.html', data)


def write_insert(request):
    # 키워드, 페이지 히스토리 전달
    kwd = request.GET.get('kwd', '')
    cur_paging_num = request.GET.get('cur_paging_num', '')

    board = Board()
    board.title = request.POST['title']
    board.contents = request.POST['content']

    user = User()
    user.id = request.session['authuser']['id']

    board.user = user

    value = Board.objects.aggregate(max_groupno=Max('group_no'))
    max_groupno = 0 if value["max_groupno"] is None else value["max_groupno"]

    board.group_no = max_groupno

    board.save()

    return HttpResponseRedirect('/board?kwd=' + kwd + '&cur_paging_num=' + cur_paging_num)


def delete(request, id=0):
    board = Board.objects.get(id=id)
    board.delete()

    return HttpResponseRedirect('/board')


def get_paging_list(paging_num_size, start_view_paging_num):
    result_list = []
    for i in range(0, paging_num_size):
        result_list.append(start_view_paging_num+i)

    return result_list
