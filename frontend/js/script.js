document.addEventListener('DOMContentLoaded', () => {
    const originalTextArea = document.getElementById('original-text');
    const currentCharCountSpan = document.getElementById('current-char-count');
    const targetAudienceSelect = document.getElementById('target-audience');
    const convertButton = document.getElementById('convert-button');
    const convertedTextArea = document.getElementById('converted-text');
    const copyButton = document.getElementById('copy-button');
    const feedbackGoodButton = document.getElementById('feedback-good');
    const feedbackBadButton = document.getElementById('feedback-bad');

    // FR-04: 입력 편의성 - 글자 수 표시
    originalTextArea.addEventListener('input', () => {
        const currentLength = originalTextArea.value.length;
        currentCharCountSpan.textContent = currentLength;
    });

    // FR-01, FR-05: 핵심 말투 변환 및 오류 처리
    convertButton.addEventListener('click', async () => {
        const originalText = originalTextArea.value;
        const targetAudience = targetAudienceSelect.value;

        if (originalText.trim() === '') {
            alert('변환할 내용을 입력해주세요.');
            return;
        }

        convertButton.disabled = true;
        convertButton.textContent = '변환 중...'; // 로딩 상태 표시

        try {
            const response = await fetch('http://localhost:5001/api/convert', { // 가상의 API 엔드포인트
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ originalText, targetAudience }),
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'API 호출에 실패했습니다.');
            }

            const data = await response.json();
            convertedTextArea.value = data.convertedText; // FR-01: 변환 결과 표시
        } catch (error) {
            console.error('변환 오류:', error);
            alert(`오류가 발생했습니다: ${error.message}
잠시 후 다시 시도해주세요.`); // FR-05: 오류 메시지 표시
            convertedTextArea.value = '변환 중 오류가 발생했습니다. 잠시 후 다시 시도해주세요.';
        } finally {
            convertButton.disabled = false;
            convertButton.textContent = '변환하기';
        }
    });

    // FR-03: 결과 활용 - 복사하기 기능
    copyButton.addEventListener('click', async () => {
        if (convertedTextArea.value.trim() === '') {
            alert('변환된 내용이 없습니다.');
            return;
        }

        try {
            await navigator.clipboard.writeText(convertedTextArea.value);
            alert('복사되었습니다!'); // FR-03: 시각적 피드백
        } catch (err) {
            console.error('클립보드 복사 실패:', err);
            alert('클립보드 복사에 실패했습니다. 수동으로 복사해주세요.');
        }
    });

    // FR-06: 사용자 피드백 (간단한 콘솔 로그로 처리)
    feedbackGoodButton.addEventListener('click', () => {
        alert('피드백 감사합니다! 서비스 개선에 반영하겠습니다.');
        console.log('User feedback: Good');
    });

    feedbackBadButton.addEventListener('click', () => {
        alert('피드백 감사합니다. 더 나은 서비스로 보답하겠습니다.');
        console.log('User feedback: Bad');
    });
});